"""Финальный этап конвейера: сохранить видео локально + уведомить владельца в Telegram."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import httpx

from config import get_settings
from utils.helpers import async_retry

_settings = get_settings()

# Telegram Bot API для прямой отправки файлов (без aiogram — конвейер работает отдельно от бота)
_TG_API = "https://api.telegram.org/bot{token}/{method}"


class NotificationClient:
    """Скачивает готовое видео, сохраняет в ./ready_to_post/ и отправляет владельцу в Telegram."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.ready_dir = Path("ready_to_post")
        self.ready_dir.mkdir(parents=True, exist_ok=True)

    @async_retry(max_retries=_settings.max_retries, delay=float(_settings.retry_delay_seconds))
    async def publish_reel(self, video_url: str, caption: str) -> dict:
        """Основной метод: скачать → сохранить → отправить владельцу."""
        # 1. Скачиваем видео
        video_path = await self._download_video(video_url)

        # 2. Сохраняем подпись рядом с видео
        caption_path = video_path.with_suffix(".txt")
        caption_path.write_text(caption, encoding="utf-8")
        self.logger.info("Подпись сохранена: %s", caption_path)

        # 3. Уведомляем владельца в Telegram
        result = await self._notify_owner(video_path, caption)
        return result

    async def _download_video(self, video_url: str) -> Path:
        """Скачивает видео и сохраняет в ./ready_to_post/."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = self.ready_dir / f"reel_{timestamp}.mp4"

        self.logger.info("Скачиваем видео: %s → %s", video_url, dest)

        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
            response = await client.get(video_url)
            response.raise_for_status()
            dest.write_bytes(response.content)

        size_mb = dest.stat().st_size / 1_048_576
        self.logger.info("Видео сохранено: %s (%.1f MB)", dest, size_mb)
        return dest

    async def _notify_owner(self, video_path: Path, caption: str) -> dict:
        """Отправляет видео + подпись владельцу через Telegram Bot API."""
        if not _settings.owner_chat_id:
            self.logger.warning("OWNER_CHAT_ID не задан — уведомление не отправлено")
            return {"status": "skipped", "reason": "OWNER_CHAT_ID not set"}

        if not _settings.telegram_bot_token:
            self.logger.warning("TELEGRAM_BOT_TOKEN не задан — уведомление не отправлено")
            return {"status": "skipped", "reason": "TELEGRAM_BOT_TOKEN not set"}

        send_url = _TG_API.format(token=_settings.telegram_bot_token, method="sendVideo")

        # Telegram ограничивает caption до 1024 символов
        short_caption = caption[:1020] + "..." if len(caption) > 1024 else caption

        self.logger.info(
            "Отправляем видео владельцу (chat_id=%s)...", _settings.owner_chat_id
        )

        async with httpx.AsyncClient(timeout=120) as client:
            with open(video_path, "rb") as f:
                response = await client.post(
                    send_url,
                    data={
                        "chat_id": _settings.owner_chat_id,
                        "caption": short_caption,
                        "supports_streaming": "true",
                    },
                    files={"video": (video_path.name, f, "video/mp4")},
                )
            response.raise_for_status()
            data = response.json()

        self.logger.info(
            "Видео отправлено владельцу. message_id=%s",
            data.get("result", {}).get("message_id"),
        )
        return data
