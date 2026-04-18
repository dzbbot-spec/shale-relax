"""Клавиатуры бота: главное меню и служебные кнопки."""

from __future__ import annotations

import os

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    WebAppInfo,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://dzbbot-spec.github.io/shale-relax")


def main_menu() -> ReplyKeyboardMarkup:
    """Главное меню с FAQ и кнопкой бронирования."""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🗺 Как добраться"),
        KeyboardButton(text="🏔 Что посмотреть"),
    )
    builder.row(
        KeyboardButton(text="🏍 Эндуро-маршруты"),
        KeyboardButton(text="🚗 Трансфер"),
    )
    builder.row(
        KeyboardButton(text="🏠 Наши домики"),
        KeyboardButton(text="📅 Забронировать"),
    )
    builder.row(
        KeyboardButton(
            text="🌐 Витрина",
            web_app=WebAppInfo(url=MINI_APP_URL),
        )
    )
    return builder.as_markup(resize_keyboard=True)


def cancel_menu() -> ReplyKeyboardMarkup:
    """Кнопка отмены во время диалога бронирования."""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ Отменить"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def remove_keyboard() -> ReplyKeyboardRemove:
    """Убрать клавиатуру (используется в начале диалога)."""
    return ReplyKeyboardRemove()
