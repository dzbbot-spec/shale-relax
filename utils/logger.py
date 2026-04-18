"""Настройка логирования: вывод в консоль и в файл одновременно."""

from __future__ import annotations

import logging
from pathlib import Path


def setup_logger(name: str, level: str = "INFO", logs_dir: str = "./logs") -> logging.Logger:
    """Создаёт логгер с двумя обработчиками: консоль + файл.

    Повторный вызов с тем же name возвращает уже настроенный логгер.
    """
    log_path = Path(logs_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    # Не добавляем обработчики повторно
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())
    logger.propagate = False

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Консоль
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    # Файл
    file_handler = logging.FileHandler(log_path / f"{name}.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
