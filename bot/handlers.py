"""Обработчики сообщений: бронирование, FAQ, приём фото от управляющего."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, PhotoSize

from bot.keyboard import cancel_menu, main_menu, remove_keyboard
from config import get_settings
from utils.helpers import format_booking
from utils.logger import setup_logger

router = Router()
_settings = get_settings()
_logger = setup_logger("bot", _settings.log_level, _settings.logs_path)

# ─── FSM: состояния диалога бронирования ───────────────────────────────────

class BookingStates(StatesGroup):
    name = State()
    dates = State()
    guests = State()
    contact = State()


# ─── FAQ: ключевые фразы → ответы ──────────────────────────────────────────

FAQ: dict[str, str] = {
    "как добраться": (
        "✈️ *Как добраться до Шале Релакс*\n\n"
        "• Ближайший аэропорт — Минеральные Воды или Нальчик\n"
        "• От Нальчика до посёлка Эльбрус ~130 км (~2,5 ч)\n"
        "• Можно заказать трансфер — напишите нам, организуем\n"
        "• На своём авто: по трассе А-158 до посёлка Эльбрус, "
        "мы в самом конце посёлка у подножия горы"
    ),
    "что посмотреть": (
        "🏔 *Что посмотреть в Приэльбрусье*\n\n"
        "• Эльбрус и Чегет — канатные дороги, смотровые площадки\n"
        "• Поляна Азау — начало маршрутов на Эльбрус\n"
        "• Озеро Донгуз-Орун и Чирюкол — пешие маршруты\n"
        "• Водопад Девичьи Косы — 20 минут от нас\n"
        "• Джилы-Су — нарзанные источники и вид на северный склон Эльбруса\n"
        "• Термальные источники в ущелье — расслабление после активного дня"
    ),
    "эндуро": (
        "🏍 *Эндуро-маршруты из Шале Релакс*\n\n"
        "• *Джилы-Су* — классика, северный склон Эльбруса, нарзаны\n"
        "• *Чегетджара* — лесные тропы и горные дороги\n"
        "• *Баксанское ущелье* — асфальт + грунтовки вдоль реки\n"
        "• *Безенги* — для опытных, дикая природа\n\n"
        "Мы можем порекомендовать проводника и аренду мотоцикла."
    ),
    "трансфер": (
        "🚗 *Трансфер*\n\n"
        "Организуем трансфер из:\n"
        "• Аэропорта Минеральные Воды\n"
        "• Аэропорта Нальчик\n"
        "• Железнодорожного вокзала Нальчик\n\n"
        "Укажите точку отправления в заявке на бронирование, "
        "и мы включим трансфер в подготовку к вашему приезду."
    ),
}


# ─── Команда /stats (только для владельца) ──────────────────────────────────

@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    if str(message.from_user.id) != _settings.owner_chat_id:
        await message.answer("⛔ Команда доступна только владельцу.")
        return

    bookings_file = Path("data/bookings.json")
    photos_dir = Path("data/photos")
    ready_dir = Path("ready_to_post")

    # Заявки
    bookings: list = []
    if bookings_file.exists():
        try:
            bookings = json.loads(bookings_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            bookings = []

    total = len(bookings)
    last_date = bookings[-1].get("created_at", "—") if bookings else "—"

    # Очередь фото
    photos_count = 0
    if photos_dir.exists():
        photos_count = len(list(photos_dir.glob("*.jpg")) + list(photos_dir.glob("*.png")))

    # Готовые видео
    videos_count = 0
    if ready_dir.exists():
        videos_count = len(list(ready_dir.glob("*.mp4")))

    text = (
        "📊 <b>Статистика Шале Релакс</b>\n"
        "─────────────────────────\n"
        f"📋 Заявок всего:       <b>{total}</b>\n"
        f"🕐 Последняя заявка:  <b>{last_date}</b>\n"
        f"📸 Фото в очереди:    <b>{photos_count}</b>\n"
        f"🎬 Видео готовых:      <b>{videos_count}</b>\n"
        "─────────────────────────"
    )
    await message.answer(text, parse_mode="HTML")


# ─── Команда /start ─────────────────────────────────────────────────────────

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Приветствие и вывод главного меню."""
    await state.clear()
    name = message.from_user.first_name or "путешественник"
    await message.answer(
        f"👋 Привет, {name}!\n\n"
        "🏔 Добро пожаловать в <b>Шале Релакс</b> — уютные домики у самого подножия Эльбруса.\n\n"
        "📍 Посёлок Эльбрус · Высота 1800 м · 5 минут до подъёмников\n\n"
        "Здесь горный воздух, тишина и вид на двуглавую вершину прямо из окна. "
        "Я помогу вам спланировать поездку, расскажу о маршрутах и оформлю заявку на проживание.\n\n"
        "Выберите, что вас интересует 👇",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


# ─── FAQ-обработчики ────────────────────────────────────────────────────────

@router.message(F.text == "🗺 Как добраться")
async def faq_route(message: Message) -> None:
    await message.answer(FAQ["как добраться"], reply_markup=main_menu(), parse_mode="Markdown")


@router.message(F.text == "🏔 Что посмотреть")
async def faq_sights(message: Message) -> None:
    await message.answer(FAQ["что посмотреть"], reply_markup=main_menu(), parse_mode="Markdown")


@router.message(F.text == "🏍 Эндуро-маршруты")
async def faq_enduro(message: Message) -> None:
    await message.answer(FAQ["эндуро"], reply_markup=main_menu(), parse_mode="Markdown")


@router.message(F.text == "🚗 Трансфер")
async def faq_transfer(message: Message) -> None:
    await message.answer(FAQ["трансфер"], reply_markup=main_menu(), parse_mode="Markdown")


# ─── Диалог бронирования ────────────────────────────────────────────────────

@router.message(F.text == "📅 Забронировать")
async def booking_start(message: Message, state: FSMContext) -> None:
    """Начало диалога: запрашиваем имя."""
    await state.set_state(BookingStates.name)
    _logger.info("booking_start: uid=%s state→name", message.from_user.id)
    await message.answer(
        "Отлично! Оформим заявку за 4 шага.\n\n"
        "<b>Шаг 1/4</b> — Как вас зовут?",
        reply_markup=cancel_menu(),
        parse_mode="HTML",
    )


@router.message(BookingStates.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """Сохраняем имя, запрашиваем даты."""
    _logger.info("process_name: uid=%s text=%r", message.from_user.id, message.text)
    if message.text == "❌ Отменить":
        await _cancel(message, state)
        return

    await state.update_data(name=message.text.strip())
    await state.set_state(BookingStates.dates)
    await message.answer(
        "<b>Шаг 2/4</b> — Укажите даты поездки\n"
        "Например: 12.05 — 15.05 или с 12 по 15 мая",
        reply_markup=cancel_menu(),
        parse_mode="HTML",
    )


@router.message(BookingStates.dates)
async def process_dates(message: Message, state: FSMContext) -> None:
    """Сохраняем даты, запрашиваем количество гостей."""
    _logger.info("process_dates: uid=%s text=%r", message.from_user.id, message.text)
    if message.text == "❌ Отменить":
        await _cancel(message, state)
        return

    await state.update_data(dates=message.text.strip())
    await state.set_state(BookingStates.guests)
    await message.answer(
        "<b>Шаг 3/4</b> — Сколько будет гостей?",
        reply_markup=cancel_menu(),
        parse_mode="HTML",
    )


@router.message(BookingStates.guests)
async def process_guests(message: Message, state: FSMContext) -> None:
    """Сохраняем кол-во гостей, запрашиваем контакт."""
    _logger.info("process_guests: uid=%s text=%r", message.from_user.id, message.text)
    if message.text == "❌ Отменить":
        await _cancel(message, state)
        return

    await state.update_data(guests=message.text.strip())
    await state.set_state(BookingStates.contact)
    await message.answer(
        "<b>Шаг 4/4</b> — Оставьте контакт для связи\n"
        "Номер телефона или Telegram @username",
        reply_markup=cancel_menu(),
        parse_mode="HTML",
    )


@router.message(BookingStates.contact)
async def process_contact(message: Message, state: FSMContext, bot: Bot) -> None:
    """Финал: сохраняем заявку, отправляем владельцу."""
    _logger.info("process_contact: uid=%s text=%r", message.from_user.id, message.text)
    if message.text == "❌ Отменить":
        await _cancel(message, state)
        return

    data = await state.get_data()
    data["contact"] = message.text.strip()
    data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    await state.clear()

    # Сохранить локально
    _save_booking(data)

    # Переслать владельцу
    if _settings.owner_chat_id:
        try:
            await bot.send_message(
                chat_id=_settings.owner_chat_id,
                text=format_booking(data),
            )
            _logger.info("Заявка отправлена владельцу (chat_id=%s)", _settings.owner_chat_id)
        except Exception as exc:  # noqa: BLE001
            _logger.error("Не удалось переслать заявку владельцу: %s", exc)
    else:
        _logger.warning("OWNER_CHAT_ID не задан — заявка не отправлена владельцу")

    await message.answer(
        "✅ <b>Заявка принята!</b>\n\n"
        "Мы свяжемся с вами в ближайшее время. "
        "Спасибо, что выбрали Шале Релакс!",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


async def _cancel(message: Message, state: FSMContext) -> None:
    """Отмена бронирования на любом шаге."""
    await state.clear()
    await message.answer("Бронирование отменено. Возвращаю в главное меню.", reply_markup=main_menu())


# ─── Приём фото от управляющего ─────────────────────────────────────────────

@router.message(F.photo)
async def receive_manager_photo(message: Message, bot: Bot) -> None:
    """Принимает фото только от авторизованного управляющего."""
    user = message.from_user
    chat_id = str(message.chat.id)
    username = (user.username or "").lower().lstrip("@")

    allowed = (
        (_settings.manager_chat_id and chat_id == _settings.manager_chat_id)
        or (_settings.manager_username and username == _settings.manager_username.lower())
    )

    if not allowed:
        await message.answer("⛔ Фото для конвейера может отправлять только управляющий.")
        return

    # Скачиваем фото наилучшего качества
    photo: PhotoSize = message.photo[-1]
    file_obj = await bot.get_file(photo.file_id)

    photos_dir = Path("data/photos")
    photos_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = photos_dir / f"{timestamp}_{photo.file_unique_id}.jpg"
    await bot.download_file(file_obj.file_path, destination=str(dest))

    _logger.info("Фото управляющего сохранено: %s", dest)
    await message.answer(f"✅ Фото принято. Файл: `{dest.name}`\nДобавлено в очередь конвейера.", parse_mode="Markdown")


# ─── Текстовый фолбэк: только когда нет активного FSM-состояния ─────────────
# StateFilter(None) гарантирует, что этот хендлер НЕ перехватит сообщения
# пока пользователь находится в диалоге бронирования.

@router.message(StateFilter(None), F.text)
async def text_fallback(message: Message) -> None:
    """Поиск по FAQ или подсказка меню. Срабатывает только вне диалога бронирования."""
    _logger.warning("text_fallback: uid=%s text=%r (state=None)", message.from_user.id, message.text)
    query = (message.text or "").lower()
    for key, answer in FAQ.items():
        if key in query:
            await message.answer(answer, reply_markup=main_menu(), parse_mode="Markdown")
            return

    await message.answer(
        "Не понял вопрос 🤔 Воспользуйтесь кнопками меню или напишите нам напрямую.",
        reply_markup=main_menu(),
    )


# ─── Вспомогательные функции ─────────────────────────────────────────────────

def _save_booking(payload: dict) -> None:
    """Сохраняет заявку в локальный JSON-архив."""
    data_file = Path("data/bookings.json")
    data_file.parent.mkdir(parents=True, exist_ok=True)

    entries: list = []
    if data_file.exists():
        try:
            entries = json.loads(data_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            entries = []

    entries.append(payload)
    data_file.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    _logger.info("Заявка сохранена локально: %s", data_file)
