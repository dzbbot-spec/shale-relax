"""Клиент Kling AI: JWT-аутентификация через Access Key + Secret Key."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import logging
import time
from pathlib import Path

import httpx

from config import get_settings
from utils.helpers import async_retry

_settings = get_settings()

# Официальные эндпоинты Kling AI API
_API_BASE = "https://api.klingai.com"
_IMAGE_TO_VIDEO_URL = f"{_API_BASE}/v1/videos/image2video"
_TASK_STATUS_URL = f"{_API_BASE}/v1/videos/image2video/{{task_id}}"


def _build_jwt(access_key: str, secret_key: str) -> str:
    """Генерирует JWT-токен для Kling AI по спецификации официального API.

    Срок действия: 30 минут. Пересоздаётся перед каждым запросом.
    """
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {
        "iss": access_key,
        "exp": now + 1800,  # истекает через 30 мин
        "nbf": now - 5,     # действителен с 5 сек назад (защита от рассинхрона часов)
    }

    def _b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

    header_enc = _b64url(json.dumps(header, separators=(",", ":")).encode())
    payload_enc = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_enc}.{payload_enc}".encode()

    signature = hmac.new(
        secret_key.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    return f"{header_enc}.{payload_enc}.{_b64url(signature)}"


class KlingClient:
    """Генерирует видео из фото через официальный Kling AI API."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.access_key = _settings.kling_access_key
        self.secret_key = _settings.kling_secret_key

    def _auth_headers(self) -> dict[str, str]:
        """Возвращает заголовки с актуальным JWT-токеном."""
        token = _build_jwt(self.access_key, self.secret_key)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    @async_retry(max_retries=_settings.max_retries, delay=float(_settings.retry_delay_seconds))
    async def generate_video(self, photo_path: Path, prompt: str) -> str:
        """Запускает генерацию видео, дожидается готовности и возвращает URL."""
        if not self.access_key or not self.secret_key:
            raise ValueError("KLING_ACCESS_KEY или KLING_SECRET_KEY не заданы в .env")

        self.logger.info("Kling: запуск генерации для %s", photo_path.name)

        # Кодируем фото в чистый base64 (без data URL префикса)
        image_b64 = base64.b64encode(photo_path.read_bytes()).decode("utf-8")

        payload = {
            "model_name": _settings.kling_model,
            "image": image_b64,
            "prompt": prompt,
            "cfg_scale": 0.5,
            "mode": "std",
            "duration": "5",
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                _IMAGE_TO_VIDEO_URL,
                headers=self._auth_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        # Kling возвращает task_id внутри data.task.id
        task_id = (
            data.get("data", {}).get("task_id")
            or data.get("data", {}).get("task", {}).get("id")
            or data.get("task_id")
        )
        if not task_id:
            raise ValueError(f"Kling не вернул task_id. Ответ: {data}")

        self.logger.info("Kling: задача создана task_id=%s. Ожидаем готовности...", task_id)
        video_url = await self._poll_until_ready(task_id)
        self.logger.info("Kling: видео готово → %s", video_url)
        return video_url

    async def _poll_until_ready(self, task_id: str) -> str:
        """Опрашивает статус задачи каждые N секунд до получения URL видео."""
        interval = _settings.kling_poll_interval
        max_attempts = _settings.kling_max_poll_attempts
        status_url = _TASK_STATUS_URL.format(task_id=task_id)

        async with httpx.AsyncClient(timeout=30) as client:
            for attempt in range(1, max_attempts + 1):
                response = await client.get(status_url, headers=self._auth_headers())
                response.raise_for_status()
                data = response.json()

                # Статус может быть в data.task_status или data.data.task_status
                task_data = data.get("data", data)
                status = str(task_data.get("task_status", "")).lower()

                self.logger.debug(
                    "Kling опрос %s/%s, статус: %s", attempt, max_attempts, status
                )

                if status in ("succeed", "completed", "done", "success"):
                    # URL может быть вложен по-разному в зависимости от версии API
                    works = task_data.get("task_result", {}).get("videos", [])
                    if works:
                        return works[0].get("url", "")
                    video_url = task_data.get("video_url") or task_data.get("result_url")
                    if video_url:
                        return video_url
                    raise ValueError(f"Статус 'succeed', но URL видео не найден: {data}")

                if status in ("failed", "error"):
                    raise ValueError(f"Kling: ошибка генерации: {data}")

                await asyncio.sleep(interval)

        raise TimeoutError(
            f"Видео не готово за {max_attempts * interval} сек (task_id={task_id})"
        )
