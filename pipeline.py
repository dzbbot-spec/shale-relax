"""ИИ-конвейер: фото -> видео -> подпись -> публикация."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import requests
from openai import OpenAI

from src.config import load_settings
from src.utils.logger import setup_logger
from src.utils.retry import retry

BANNED_WORDS = ("аренда", "бронирование", "цена", "стоимость")


class ContentPipeline:
    """Инкапсулирует все этапы обработки и публикации контента."""

    def __init__(self) -> None:
        self.settings = load_settings()
        self.logger = setup_logger("pipeline", self.settings.log_level)
        self.client = OpenAI(api_key=self.settings.openai_api_key) if self.settings.openai_api_key else None

    def run(self) -> None:
        """Обрабатывает очередь фото по одному, с подробным логированием."""
        photos_dir = Path("data/photos")
        photos_dir.mkdir(parents=True, exist_ok=True)

        photo_files = sorted(photos_dir.glob("*.jpg")) + sorted(photos_dir.glob("*.png"))
        if not photo_files:
            self.logger.info("Очередь фотографий пуста, обработка не требуется.")
            return

        self.logger.info("Найдено %s фото в очереди.", len(photo_files))

        for photo_path in photo_files:
            self.logger.info("Старт обработки файла: %s", photo_path.name)
            try:
                video_url = self.generate_video(photo_path)
                caption = self.generate_caption(photo_path.name)
                self.publish_reel(video_url, caption)
                self.archive_processed_photo(photo_path)
                self.logger.info("Файл обработан успешно: %s", photo_path.name)
            except Exception as error:  # noqa: BLE001
                self.logger.error("Ошибка обработки %s: %s", photo_path.name, error)

    @property
    def _retry(self):
        return retry(
            max_retries=self.settings.max_retries,
            delay_seconds=self.settings.retry_delay_seconds,
            logger=self.logger,
        )

    def _headers(self, api_key: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _request_json(self, method: str, url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.request(method=method, url=url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    def generate_video(self, photo_path: Path) -> str:
        """Вызывает API Kling (Umnik.ai) и возвращает URL сгенерированного видео."""

        @self._retry
        def _generate() -> str:
            if not self.settings.kling_api_url or not self.settings.kling_api_key:
                raise ValueError("Не настроены KLING_API_URL или KLING_API_KEY")

            payload = {
                "model": self.settings.kling_model,
                "image_path": str(photo_path.resolve()),
                "prompt": "Cinematic mountain atmosphere, soft morning light, smooth camera movement",
            }
            data = self._request_json(
                method="POST",
                url=self.settings.kling_api_url,
                headers=self._headers(self.settings.kling_api_key),
                payload=payload,
            )

            video_url = data.get("video_url")
            if not video_url:
                raise ValueError("API Kling не вернул video_url")
            return video_url

        return _generate()

    def generate_caption(self, source_name: str) -> str:
        """Генерирует атмосферную подпись с фильтрацией запрещенных слов."""

        @self._retry
        def _caption() -> str:
            if not self.client:
                raise ValueError("Не задан OPENAI_API_KEY")

            prompt = (
                "Ты — SMM-менеджер аккаунта @shale_relax_elbrus. "
                "Пиши атмосферные подписи для рилсов про Приэльбрусье и домики Шале Релакс. "
                "Без слов: аренда, бронирование, цена, стоимость. "
                "Только атмосфера, природа, эмоции. 2-3 коротких предложения. "
                "3-5 хэштегов. Геотег: Поселок Эльбрус. "
                f"Исходный файл: {source_name}."
            )

            completion = self.client.responses.create(
                model=self.settings.openai_model,
                input=prompt,
            )
            text = completion.output_text.strip()

            lowered = text.lower()
            if any(word in lowered for word in BANNED_WORDS):
                raise ValueError("GPT сгенерировал подпись с запрещенными словами")
            return text

        return _caption()

    def publish_reel(self, video_url: str, caption: str) -> None:
        """Публикует готовый рилс в Instagram через Smmbox API."""

        @self._retry
        def _publish() -> None:
            required_fields = [
                self.settings.smmbox_api_url,
                self.settings.smmbox_api_key,
                self.settings.smmbox_project_id,
                self.settings.smmbox_account_id,
            ]
            if not all(required_fields):
                raise ValueError("Не настроены параметры SMMBOX_API_* в .env")

            payload = {
                "project_id": self.settings.smmbox_project_id,
                "account_id": self.settings.smmbox_account_id,
                "video_url": video_url,
                "caption": caption,
            }
            self._request_json(
                method="POST",
                url=self.settings.smmbox_api_url,
                headers=self._headers(self.settings.smmbox_api_key),
                payload=payload,
            )

        _publish()

    def archive_processed_photo(self, photo_path: Path) -> None:
        """Перемещает успешно обработанное фото в архив."""
        archive_dir = Path("data/photos/processed")
        archive_dir.mkdir(parents=True, exist_ok=True)
        destination = archive_dir / photo_path.name
        photo_path.rename(destination)
        self.logger.info("Файл перемещен в архив: %s", destination)


if __name__ == "__main__":
    pipeline = ContentPipeline()
    pipeline.run()
