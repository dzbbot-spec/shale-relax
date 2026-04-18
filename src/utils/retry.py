"""Простой декоратор retry для сетевых операций."""

from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def retry(max_retries: int, delay_seconds: int, logger) -> Callable[[F], F]:
    """Повторяет выполнение функции при исключении до max_retries раз."""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = max_retries + 1
            for current_attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:  # noqa: BLE001
                    if current_attempt >= attempts:
                        logger.error(
                            "Операция '%s' завершилась ошибкой после %s попыток: %s",
                            func.__name__,
                            attempts,
                            error,
                        )
                        raise

                    logger.warning(
                        "Ошибка в '%s' (попытка %s/%s): %s. Повтор через %s сек.",
                        func.__name__,
                        current_attempt,
                        attempts,
                        error,
                        delay_seconds,
                    )
                    time.sleep(delay_seconds)

        return wrapper  # type: ignore[return-value]

    return decorator
