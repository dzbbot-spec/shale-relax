"""Генерация атмосферных подписей через OpenAI Chat Completions."""

from __future__ import annotations

import logging
import random
from pathlib import Path

from openai import AsyncOpenAI

from config import BANNED_WORDS, GPT_SYSTEM_PROMPT_FILE, PUBLICATION_SCHEDULE, get_settings
from utils.helpers import async_retry

_settings = get_settings()


def _load_system_prompt() -> str:
    """Читает системный промпт из файла, с фоллбэком на встроенный."""
    if GPT_SYSTEM_PROMPT_FILE.exists():
        return GPT_SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()

    # Встроенный промпт на случай отсутствия файла
    return (
        "Ты — контент-менеджер аккаунта @shale_relax_elbrus в Instagram. "
        "Пишешь атмосферные подписи к видео про Приэльбрусье и горный отдых. "
        "ЗАПРЕЩЕНО использовать слова: аренда, бронирование, цена, стоимость, заказать, купить. "
        "Пиши только про природу, атмосферу, ощущения, эмоции. "
        "Формат: 2–3 коротких предложения + 5–7 хэштегов на русском + геотег 'Поселок Эльбрус'. "
        "Стиль: живой, тёплый, без штампов."
    )


class GPTClient:
    """Генерирует подписи через OpenAI, с фильтрацией запрещённых слов."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.client = AsyncOpenAI(api_key=_settings.openai_api_key) if _settings.openai_api_key else None
        self.system_prompt = _load_system_prompt()

    @async_retry(max_retries=_settings.max_retries, delay=_settings.retry_delay_seconds)
    async def generate_caption(self, photo_name: str, rubric: str | None = None) -> str:
        """Генерирует подпись. Повторяет, если GPT использовал запрещённые слова."""
        if not self.client:
            raise ValueError("OPENAI_API_KEY не задан в .env")

        # Выбираем рубрику: из параметра или случайную из расписания
        rubric_info = rubric or random.choice(PUBLICATION_SCHEDULE)["rubric"]

        user_prompt = (
            f"Рубрика сегодня: {rubric_info}. "
            f"Напиши подпись для видео (исходное фото: {photo_name}). "
            "Не забудь хэштеги и геотег."
        )

        self.logger.info("GPT: генерация подписи для '%s' (рубрика: %s)", photo_name, rubric_info)

        response = await self.client.chat.completions.create(
            model=_settings.openai_model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
            max_tokens=300,
        )

        caption = response.choices[0].message.content.strip()

        # Проверяем на запрещённые слова
        if any(word in caption.lower() for word in BANNED_WORDS):
            banned_found = [w for w in BANNED_WORDS if w in caption.lower()]
            raise ValueError(
                f"GPT использовал запрещённые слова: {banned_found}. Будет повторная попытка."
            )

        self.logger.info("GPT: подпись готова (%s символов)", len(caption))
        return caption
