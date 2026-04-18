"""Telegram-бот проекта Шале Релакс."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.config import load_settings
from src.utils.logger import setup_logger

ASK_NAME, ASK_DATES, ASK_GUESTS, ASK_CONTACT = range(4)

FAQ_ANSWERS = {
    "как добраться": (
        "До Шале Релакс обычно едут через Минеральные Воды или Нальчик, "
        "затем трансфером/такси до поселка Эльбрус."
    ),
    "что посмотреть": (
        "Рядом: гора Эльбрус, поляна Азау, Чегет, экотропы, канатные дороги "
        "и смотровые точки с видом на Кавказский хребет."
    ),
    "эндуро-маршруты": (
        "Есть живописные маршруты по горным дорогам и лесным тропам Приэльбрусья. "
        "Подскажем варианты по уровню подготовки."
    ),
    "трансфер": (
        "Можно организовать трансфер от аэропорта/вокзала до Шале Релакс. "
        "Уточните удобную точку старта в заявке."
    ),
}


def faq_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с FAQ-разделами и стартом бронирования."""
    keyboard = [
        ["Как добраться", "Что посмотреть"],
        ["Эндуро-маршруты", "Трансфер"],
        ["Забронировать"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение бота."""
    context.user_data.clear()
    await update.message.reply_text(
        "Добро пожаловать в Шале Релакс. Выберите вопрос из меню или нажмите 'Забронировать'.",
        reply_markup=faq_keyboard(),
    )


async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ответы на популярные вопросы по ключевым фразам."""
    user_message = (update.message.text or "").strip().lower()
    for key, answer in FAQ_ANSWERS.items():
        if key in user_message:
            await update.message.reply_text(answer, reply_markup=faq_keyboard())
            return


async def booking_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Первый шаг сценария бронирования: запрашиваем имя."""
    context.user_data["booking"] = {}
    await update.message.reply_text("Как вас зовут?", reply_markup=ReplyKeyboardRemove())
    return ASK_NAME


async def ask_dates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняем имя и просим даты заезда/выезда."""
    context.user_data["booking"]["name"] = update.message.text.strip()
    await update.message.reply_text("Укажите даты поездки (например: 12.05-15.05)")
    return ASK_DATES


async def ask_guests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняем даты и просим количество гостей."""
    context.user_data["booking"]["dates"] = update.message.text.strip()
    await update.message.reply_text("Сколько будет гостей?")
    return ASK_GUESTS


async def ask_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняем количество гостей и просим контакт для связи."""
    context.user_data["booking"]["guests"] = update.message.text.strip()
    await update.message.reply_text("Оставьте контакт для связи (телефон или @username)")
    return ASK_CONTACT


async def booking_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершаем заявку, отправляем владельцу и сохраняем локально."""
    settings = context.bot_data["settings"]
    logger = context.bot_data["logger"]

    context.user_data["booking"]["contact"] = update.message.text.strip()
    payload = context.user_data["booking"]

    message = (
        "Новая заявка на бронирование:\n"
        f"Имя: {payload['name']}\n"
        f"Даты: {payload['dates']}\n"
        f"Гостей: {payload['guests']}\n"
        f"Контакт: {payload['contact']}\n"
        f"Дата заявки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Отправляем владельцу по chat_id, если он указан в .env.
    if settings.owner_chat_id:
        try:
            await context.bot.send_message(chat_id=settings.owner_chat_id, text=message)
        except Exception as error:  # noqa: BLE001
            logger.error("Не удалось отправить заявку владельцу: %s", error)
    else:
        logger.warning("OWNER_CHAT_ID не задан. Заявка не отправлена владельцу автоматически.")

    save_booking(payload)

    await update.message.reply_text(
        (
            "Спасибо! Ваша заявка принята и передана владельцу. "
            "Мы свяжемся с вами в ближайшее время."
        ),
        reply_markup=faq_keyboard(),
    )

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена оформления заявки."""
    context.user_data.clear()
    await update.message.reply_text("Бронирование отменено.", reply_markup=faq_keyboard())
    return ConversationHandler.END


def save_booking(payload: dict) -> None:
    """Сохраняет заявки в локальный JSON-архив."""
    data_file = Path("data/bookings.json")
    data_file.parent.mkdir(parents=True, exist_ok=True)

    current = []
    if data_file.exists():
        try:
            current = json.loads(data_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            current = []

    payload = dict(payload)
    payload["created_at"] = datetime.now().isoformat(timespec="seconds")
    current.append(payload)
    data_file.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")


async def receive_manager_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Принимает фото от управляющего и складывает в очередь конвейера."""
    settings = context.bot_data["settings"]
    logger = context.bot_data["logger"]

    user = update.effective_user
    username = (user.username or "").lower()
    chat_id = str(update.effective_chat.id)

    allowed_by_chat = bool(settings.manager_chat_id) and chat_id == settings.manager_chat_id
    allowed_by_username = bool(settings.manager_username) and username == settings.manager_username.lower()

    if not (allowed_by_chat or allowed_by_username):
        await update.message.reply_text("Фото для конвейера может отправлять только управляющий.")
        return

    photo = update.message.photo[-1]
    file_obj = await context.bot.get_file(photo.file_id)

    photos_dir = Path("data/photos")
    photos_dir.mkdir(parents=True, exist_ok=True)

    file_path = photos_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.file_unique_id}.jpg"
    await file_obj.download_to_drive(custom_path=str(file_path))

    logger.info("Фото управляющего сохранено: %s", file_path)
    await update.message.reply_text("Фото принято. Добавлено в очередь ИИ-конвейера.")


def build_application() -> Application:
    """Собирает приложение Telegram-бота с обработчиками."""
    settings = load_settings()
    logger = setup_logger("bot", settings.log_level)

    if not settings.telegram_bot_token:
        raise ValueError("В .env не задан TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(settings.telegram_bot_token).build()
    app.bot_data["settings"] = settings
    app.bot_data["logger"] = logger

    booking_flow = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r"^Забронировать$"), booking_start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_dates)],
            ASK_DATES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_guests)],
            ASK_GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contact)],
            ASK_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, booking_finish)],
        },
        fallbacks=[CommandHandler("cancel", cancel_booking)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(booking_flow)
    app.add_handler(MessageHandler(filters.PHOTO, receive_manager_photo))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_faq,
        )
    )
    return app


def main() -> None:
    """Точка входа для запуска long polling."""
    try:
        application = build_application()
    except ValueError as error:
        logger = setup_logger("bot", "INFO")
        logger.error("Бот не запущен: %s", error)
        return

    logger = application.bot_data["logger"]
    logger.info("Бот запущен и готов принимать сообщения.")
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as error:  # noqa: BLE001
        logger.error("Бот остановлен из-за сетевой или конфигурационной ошибки: %s", error)


if __name__ == "__main__":
    main()
