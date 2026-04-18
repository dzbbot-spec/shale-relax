import json
import os
from datetime import datetime
from pathlib import Path

OBSIDIAN_FILE = "/Users/annakucenko/Documents/Obsidian Vault/Шале Релакс.md"
BOOKINGS_FILE = "/Users/annakucenko/shale-relax/data/bookings.json"
PHOTOS_DIR = "/Users/annakucenko/shale-relax/data/photos"
READY_DIR = "/Users/annakucenko/shale-relax/ready_to_post"


def count_files(directory):
    try:
        return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    except FileNotFoundError:
        return 0


def load_bookings():
    try:
        with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_last_booking_date(bookings):
    if not bookings:
        return "нет заявок"
    last = bookings[-1]
    date = last.get("date") or last.get("created_at") or last.get("timestamp", "")
    return date[:10] if date else "неизвестно"


def sync():
    bookings = load_bookings()
    total_bookings = len(bookings)
    last_date = get_last_booking_date(bookings)
    photos_count = count_files(PHOTOS_DIR)
    videos_count = count_files(READY_DIR)
    updated_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    content = f"""# Шале Релакс — Проект

## Статус: 🟢 Бот работает на Railway

Последнее обновление: **{updated_at}**

---

## Статистика

| Показатель | Значение |
|------------|----------|
| Заявок всего | {total_bookings} |
| Последняя заявка | {last_date} |
| Фото в очереди | {photos_count} |
| Видео готово к публикации | {videos_count} |

---

## Ключевые данные

- **Telegram бот:** @shale_relax_bot
- **Instagram:** @shale_relax_elbrus
- **Владелец:** @shale_relax_elbrus (chat_id: 1914219730)
- **Хостинг:** Railway (триал до 11 мая 2026)
- **GitHub:** dzbbot-spec/shale-relax
- **Папка проекта:** ~/shale-relax

---

## Сервисы

| Сервис | Статус | Сумма |
|--------|--------|-------|
| Railway | ✅ Активен (триал) | ~500 руб/мес |
| Telegram Bot | ✅ Активен | бесплатно |
| OpenAI API | ⚠️ Нет баланса | пополнить $5 |
| Kling AI | ⚠️ Нет баланса | пополнить |
| Smmbox | ❌ Не подключён | 1700 руб/мес |

---

## Следующие шаги

- [ ] Пополнить OpenAI ($5)
- [ ] Пополнить Kling AI
- [ ] Оплатить Railway до 11 мая
- [ ] Добавить MANAGER_CHAT_ID в .env
- [ ] Протестировать конвейер фото → видео
- [ ] Подключить Smmbox (второй этап)
- [ ] Первый пост в Instagram (второй этап)

---

## Архитектура

- **main.py** — запуск бота
- **bot/handlers.py** — бронирование + FAQ
- **pipeline/kling.py** — генерация видео
- **pipeline/gpt.py** — генерация подписей
- **scheduler.py** — автозапуск пн-вс 10:00–12:00 МСК
"""

    with open(OBSIDIAN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Obsidian обновлён: {updated_at} | Заявок: {total_bookings} | Фото: {photos_count} | Видео: {videos_count}")


if __name__ == "__main__":
    sync()
