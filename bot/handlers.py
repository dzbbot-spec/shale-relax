

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


@router.message(F.text == "🏠 Наши домики")
async def faq_chalet(message: Message) -> None:
    await message.answer(FAQ["домик"], reply_markup=main_menu(), parse_mode="Markdown")


# ─── Диалог бронирования ────────────────────────────────────────────────────

@router.message(F.text == "📅 Забронировать")
async def booking_start(message: Message, state: FSMContext) -> None:
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
    _logger.info("process_contact: uid=%s text=%r", message.from_user.id, message.text)
    if message.text == "❌ Отменить":
        await _cancel(message, state)
        return

    data = await state.get_data()
    data["contact"] = message.text.strip()
    data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await state.clear()

    _save_booking(data)

    if _settings.owner_chat_id:
        try:
            await bot.send_message(
                chat_id=_settings.owner_chat_id,
                text=format_booking(data),
            )
            _logger.info("Заявка отправлена владельцу (chat_id=%s)", _settings.owner_chat_id)
        except Exception as exc:
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
    await state.clear()
    await message.answer("Бронирование отменено. Возвращаю в главное меню.", reply_markup=main_menu())


# ─── Приём фото от управляющего ─────────────────────────────────────────────

@router.message(F.photo)
async def receive_manager_photo(message: Message, bot: Bot) -> None:
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

    photo: PhotoSize = message.photo[-1]
    file_obj = await bot.get_file(photo.file_id)

    photos_dir = Path("data/photos")
    photos_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = photos_dir / f"{timestamp}_{photo.file_unique_id}.jpg"
    await bot.download_file(file_obj.file_path, destination=str(dest))

    _logger.info("Фото управляющего сохранено: %s", dest)
    await message.answer(f"✅ Фото принято. Файл: `{dest.name}`\nДобавлено в очередь конвейера.", parse_mode="Markdown")


# ─── Текстовый фолбэк ────────────────────────────────────────────────────────

@router.message(StateFilter(None), F.text)
async def text_fallback(message: Message) -> None:
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
