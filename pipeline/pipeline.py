"""Главный оркестратор ИИ-конвейера: фото → видео → подпись → публикация."""

from __future__ import annotations

import asyncio
import json
import random
from pathlib import Path

from config import KLING_PROMPTS_FILE, get_settings
from pipeline.gpt import GPTClient
from pipeline.kling import KlingClient
from pipeline.smmbox import DeliveryClient
from utils.logger import setup_logger

_settings = get_settings()
_logger = setup_logger("pipeline", _settings.log_level, _settings.logs_path)


def _load_kling_prompts() -> list[str]:
    """Загружает библиотеку промптов Kling из JSON-файла."""
    if KLING_PROMPTS_FILE.exists():
        try:
            data = json.loads(KLING_PROMPTS_FILE.read_text(encoding="utf-8"))
            prompts = data if isinstance(data, list) else data.get("prompts", [])
            if prompts:
                return [p if isinstance(p, str) else p.get("prompt", "") for p in prompts]
        except (json.JSONDecodeError, KeyError):
            pass

    # Фоллбэк: встроенные промпты
    return [
        "Cinematic mountain atmosphere, Elbrus peak, soft morning light, slow camera pan",
        "Cozy wooden chalet in Caucasus mountains, warm interior light, gentle snowfall",
        "Epic aerial view of Baksan valley, golden hour, smooth drone movement",
        "Alpine lake reflection, crystal clear water, misty morning, slow zoom in",
        "Mountain trail in Prielbrusye, autumn colors, serene atmosphere, gentle breeze",
    ]


async def run_pipeline() -> None:
    """Обрабатывает всю очередь фото в папке data/photos/."""
    photos_dir = Path("data/photos")
    photos_dir.mkdir(parents=True, exist_ok=True)

    photo_files = sorted(photos_dir.glob("*.jpg")) + sorted(photos_dir.glob("*.png"))

    if not photo_files:
        _logger.info("Очередь пуста — нет фото для обработки.")
        return

    _logger.info("Найдено %d фото в очереди. Начинаем конвейер.", len(photo_files))

    kling = KlingClient(logger=_logger)
    gpt = GPTClient(logger=_logger)
    delivery = DeliveryClient(logger=_logger)
    kling_prompts = _load_kling_prompts()

    for photo_path in photo_files:
        _logger.info("── Обработка: %s ──", photo_path.name)
        try:
            # Шаг 1: генерация видео через Kling AI
            prompt = random.choice(kling_prompts)
            _logger.info("Промпт Kling: %s", prompt)
            video_url = await kling.generate_video(photo_path, prompt)

            # Шаг 2: генерация подписи через GPT
            caption = await gpt.generate_caption(photo_path.name)

            # Шаг 3: сохранить в ./ready_to_post/ и уведомить владельца
            await delivery.publish_reel(video_url, caption)

            # Шаг 4: архивируем обработанное фото
            _archive(photo_path)

            _logger.info("✓ Успешно обработан: %s", photo_path.name)

        except Exception as exc:  # noqa: BLE001
            _logger.error("✗ Ошибка при обработке %s: %s", photo_path.name, exc)
            # Продолжаем следующее фото, не прерываем весь конвейер


def _archive(photo_path: Path) -> None:
    """Перемещает обработанное фото в архив."""
    archive_dir = Path("data/photos/processed")
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / photo_path.name
    photo_path.rename(dest)
    _logger.info("Фото архивировано: %s", dest)


if __name__ == "__main__":
    asyncio.run(run_pipeline())
