"""Клиент Runway AI: генерация видео из фото через Gen-4 Turbo API."""

from __future__ import annotations

import asyncio
import base64
import logging
from pathlib import Path

import httpx

from config import get_settings
from utils.helpers import async_retry

_settings = get_settings()

_API_BASE = "https://api.dev.runwayml.com/v1"
_GENERATE_URL = f"{_API_BASE}/image_to_video"
_TASK_URL = f"{_API_BASE}/tasks/{{task_id}}"


class RunwayClient:
    """Генерирует видео из фото через Runway Gen-4 Turbo API."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.api_key = _settings.runway_api_key

    def _auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-11-06",
        }

    @async_retry(max_retries=_settings.max_retries, delay=float(_settings.retry_delay_seconds))
    async def generate_video(self, photo_path: Path, prompt: str) -> str:
        """Запускает генерацию видео, дожидается готовности и возвращает URL."""
        if not self.api_key:
            raise ValueError("RUNWAY_API_KEY не задан в .env")

        self.logger.info("Runway: запуск генерации для %s", photo_path.name)

        # Кодируем фото в base64 data URL
        image_bytes = photo_path.read_bytes()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        suffix = photo_path.suffix.lower().lstrip(".")
        mime = "image/jpeg" if suffix in ("jpg", "jpeg") else f"image/{suffix}"
        image_data_url = f"data:{mime};base64,{image_b64}"

        payload = {
            "model": _settings.runway_model,
            "promptImage": image_data_url,
            "promptText": prompt,
            "duration": 5,
            "ratio": "1280:720",
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                _GENERATE_URL,
                headers=self._auth_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        task_id = data.get("id")
        if not task_id:
            raise ValueError(f"Runway не вернул task id. Ответ: {data}")

        self.logger.info("Runway: задача создана id=%s. Ожидаем готовности...", task_id)
        video_url = await self._poll_until_ready(task_id)
        self.logger.info("Runway: видео готово → %s", video_url)
        return video_url

    async def _poll_until_ready(self, task_id: str) -> str:
        """Опрашивает статус задачи каждые N секунд до получения URL видео."""
        interval = _settings.runway_poll_interval
        max_attempts = _settings.runway_max_poll_attempts
        status_url = _TASK_URL.format(task_id=task_id)

        async with httpx.AsyncClient(timeout=30) as client:
            for attempt in range(1, max_attempts + 1):
                response = await client.get(status_url, headers=self._auth_headers())
                response.raise_for_status()
                data = response.json()

                status = str(data.get("status", "")).lower()
                self.logger.debug(
                    "Runway опрос %s/%s, статус: %s", attempt, max_attempts, status
                )

                if status == "succeeded":
                    outputs = data.get("output", [])
                    if outputs:
                        return outputs[0]
                    raise ValueError(f"Runway: статус succeeded, но output пуст: {data}")

                if status in ("failed", "cancelled"):
                    raise ValueError(f"Runway: ошибка генерации: {data}")

                await asyncio.sleep(interval)

        raise TimeoutError(
            f"Видео не готово за {max_attempts * interval} сек (task_id={task_id})"
        )
