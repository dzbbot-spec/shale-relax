"""Централизованная конфигурация проекта."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    telegram_bot_token: str
    owner_chat_id: str
    owner_username: str
    manager_chat_id: str
    manager_username: str
    openai_api_key: str
    openai_model: str
    kling_api_url: str
    kling_api_key: str
    kling_model: str
    smmbox_api_url: str
    smmbox_api_key: str
    smmbox_project_id: str
    smmbox_account_id: str
    max_retries: int
    retry_delay_seconds: int
    log_level: str
    msk_timezone: str


def load_settings() -> Settings:
    """Читает все параметры окружения и возвращает объект настроек."""
    return Settings(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
        owner_chat_id=os.getenv("OWNER_CHAT_ID", "").strip(),
        owner_username=os.getenv("OWNER_USERNAME", "@shale_relax_elbrus").strip(),
        manager_chat_id=os.getenv("MANAGER_CHAT_ID", "").strip(),
        manager_username=os.getenv("MANAGER_USERNAME", "").strip().lstrip("@"),
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
        kling_api_url=os.getenv("KLING_API_URL", "").strip(),
        kling_api_key=os.getenv("KLING_API_KEY", "").strip(),
        kling_model=os.getenv("KLING_MODEL", "kling-v1").strip(),
        smmbox_api_url=os.getenv("SMMBOX_API_URL", "").strip(),
        smmbox_api_key=os.getenv("SMMBOX_API_KEY", "").strip(),
        smmbox_project_id=os.getenv("SMMBOX_PROJECT_ID", "").strip(),
        smmbox_account_id=os.getenv("SMMBOX_ACCOUNT_ID", "").strip(),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        retry_delay_seconds=int(os.getenv("RETRY_DELAY_SECONDS", "5")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper().strip(),
        msk_timezone=os.getenv("MSK_TIMEZONE", "Europe/Moscow").strip(),
    )
