"""Вспомогательные функции общего назначения."""

from __future__ import annotations

import asyncio
import functools
import logging
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def async_retry(max_retries: int = 3, delay: float = 5.0, logger: logging.Logger | None = None):
    """Декоратор: повторяет async-функцию при исключении до max_retries раз."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_error: Exception | None = None
            for attempt in range(1, max_retries + 2):
                try:
                    return await func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    if attempt > max_retries:
                        if logger:
                            logger.error(
                                "Функция '%s' завершилась ошибкой после %s попыток: %s",
                                func.__name__, max_retries + 1, exc,
                            )
                        raise
                    if logger:
                        logger.warning(
                            "Ошибка в '%s' (попытка %s/%s): %s. Повтор через %.0f сек.",
                            func.__name__, attempt, max_retries + 1, exc, delay,
                        )
                    await asyncio.sleep(delay)
            raise last_error  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator


def format_booking(payload: dict) -> str:
    """Форматирует заявку в читаемое текстовое сообщение."""
    return (
        "📋 Новая заявка на бронирование\n"
        "─────────────────────────\n"
        f"👤 Имя:     {payload.get('name', '—')}\n"
        f"📅 Даты:    {payload.get('dates', '—')}\n"
        f"👥 Гостей:  {payload.get('guests', '—')}\n"
        f"📞 Контакт: {payload.get('contact', '—')}\n"
        f"🕐 Время:   {payload.get('created_at', '—')}\n"
        "─────────────────────────"
    )
