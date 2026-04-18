"""Централизованная конфигурация проекта через pydantic-settings."""

from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Все параметры берутся из .env-файла. Чувствительные данные никогда не хардкодятся."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Telegram ---
    telegram_bot_token: str = Field(default="", description="Токен бота от @BotFather")
    owner_chat_id: str = Field(default="", description="Chat ID владельца для пересылки заявок")
    owner_username: str = Field(default="@shale_relax_elbrus")
    manager_chat_id: str = Field(default="", description="Chat ID управляющего, присылающего фото")
    manager_username: str = Field(default="", description="Username управляющего (без @)")

    # --- OpenAI ---
    openai_api_key: str = Field(default="")
    openai_model: str = Field(default="gpt-4o-mini")

    # --- Kling AI (официальный API, JWT-аутентификация) ---
    kling_api_url: str = Field(default="https://api.klingai.com/v1/images/kolors-virtual-try-on")
    kling_access_key: str = Field(default="")
    kling_secret_key: str = Field(default="")
    kling_model: str = Field(default="kling-v1-5")
    kling_poll_interval: int = Field(default=15, description="Интервал опроса готовности видео (сек)")
    kling_max_poll_attempts: int = Field(default=40, description="Максимум попыток опроса (40*15=10 мин)")

    # --- Smmbox ---
    smmbox_api_url: str = Field(default="https://smmbox.com/api/v2/posts")
    smmbox_api_key: str = Field(default="")
    smmbox_account_id: str = Field(default="")

    # --- Логирование ---
    log_level: str = Field(default="INFO")
    logs_path: str = Field(default="./logs", alias="LOGS_PATH")

    # --- Пути ---
    download_path: str = Field(default="./downloads", alias="DOWNLOAD_PATH")

    # --- Повторные попытки ---
    max_retries: int = Field(default=3)
    retry_delay_seconds: int = Field(default=5)

    # --- Расписание ---
    timezone: str = Field(default="Europe/Moscow")

    # --- Режим отладки ---
    debug: bool = Field(default=False)


# Расписание публикаций по дням недели (рубрики из ТЗ 5.4)
PUBLICATION_SCHEDULE: List[dict] = [
    {"day": "mon", "hour": 10, "rubric": "Природа и виды", "hashtags": "#Эльбрус #Приэльбрусье #горы"},
    {"day": "tue", "hour": 10, "rubric": "Жизнь домиков", "hashtags": "#ШалеРелакс #уютныйдом #горскийотдых"},
    {"day": "wed", "hour": 11, "rubric": "Активности", "hashtags": "#эндуро #лыжи #Чегет #горнолыжка"},
    {"day": "thu", "hour": 10, "rubric": "Партнёры и инфра", "hashtags": "#Приэльбрусье #термальные #трансфер"},
    {"day": "fri", "hour": 11, "rubric": "Атмосфера вечера", "hashtags": "#горнаяатмосфера #вечер #звёзды"},
    {"day": "sat", "hour": 10, "rubric": "Выходной контент", "hashtags": "#отдых #горы #weekend"},
    {"day": "sun", "hour": 12, "rubric": "Итоги недели / UGC", "hashtags": "#Кабардино #КБР #природа"},
]

# Слова, запрещённые в подписях (требование ФЗ-72 и концепции аккаунта)
BANNED_WORDS = ("аренда", "бронирование", "цена", "стоимость", "заказать", "купить")

# Промпт-файлы
PROMPTS_DIR = Path("prompts")
GPT_SYSTEM_PROMPT_FILE = PROMPTS_DIR / "system_prompt_gpt.txt"
KLING_PROMPTS_FILE = PROMPTS_DIR / "kling_prompts.json"


def get_settings() -> Settings:
    """Возвращает объект настроек, загруженных из .env."""
    return Settings()
