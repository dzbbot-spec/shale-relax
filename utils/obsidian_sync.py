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
            return data if isinstance(data, list) else []
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

## Статус: 🟢 Бот + Мини-апп работают

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

| Параметр | Значение |
|----------|----------|
| Telegram бот | @shale_relax_bot |
| Instagram | @shale_relax_elbrus |
| Владелец chat_id | 1914219730 |
| GitHub | github.com/dzbbot-spec/shale-relax (публичный) |
| Railway (бот + API) | worker-production-8fd9.up.railway.app |
| Мини-апп (GitHub Pages) | dzbbot-spec.github.io/shale-relax |
| Cloudinary | dfbhw1rfx |
| Папка проекта | ~/shale-relax |

---

## Сервисы

| Сервис | Статус | Стоимость |
|--------|--------|-----------|
| Railway | ✅ Активен (триал до ~11 мая 2026) | ~500 руб/мес после |
| GitHub Pages | ✅ Активен | бесплатно |
| Cloudinary | ✅ 24 фото загружены | бесплатно |
| Telegram Bot | ✅ Активен | бесплатно |
| OpenAI API | ⚠️ Нет баланса | пополнить $5 |
| Kling AI | ⚠️ Нет баланса | пополнить |
| Smmbox | ❌ Не подключён | 1700 руб/мес |

---

## Следующие шаги

- [ ] Протестировать форму бронирования в Telegram на iPhone
- [ ] Оплатить Railway до ~11 мая 2026
- [ ] Пополнить OpenAI API ($5)
- [ ] Пополнить Kling AI
- [ ] Добавить MANAGER_CHAT_ID в Railway env
- [ ] Подключить Smmbox после оплаты тарифа

---

## Архитектура

### Бот + API (Railway)
- **main.py** — бот + aiohttp HTTP-сервер + APScheduler
- **bot/handlers.py** — FSM бронирование + FAQ + приём фото
- **bot/keyboard.py** — меню + кнопка мини-аппа
- **POST /api/booking** — приём заявок из мини-аппа → Telegram владельцу

### Мини-апп (React + Vite → GitHub Pages)
- 4 страницы: Главная, Галерея, О домиках, Заявка
- Навигация iOS-стиль (белая панель + blur)
- Слайдер со свайпом, без автопрокрутки
- Форма отправляет на Railway API
- Фото из Cloudinary (q_auto,f_auto,w_800)
- Автодеплой: GitHub Actions при пуше в main

### ИИ-конвейер (код готов, ключи не пополнены)
- **pipeline/kling.py** — Kling AI: фото → видео
- **pipeline/gpt.py** — OpenAI GPT: атмосферная подпись
- **pipeline/smmbox.py** — Smmbox: публикация в Instagram
- Расписание: пн-вс 10:00, 11:00, 12:00 МСК

---

## Решённые проблемы

| Проблема | Решение |
|----------|---------|
| Railway 404 | Procfile worker: → web: |
| GitHub Pages не деплоился | Репо приватное → публичное |
| iOS автозум при вводе | fontSize 16px + maximum-scale=1 |
| Поля дат обрезались | Убран grid, type="date" напрямую |
| Неверный Railway URL | shale-relax-production → worker-production-8fd9 |
| CORS блокировал запросы | github.io добавлен в ALLOWED_ORIGINS |
"""

    with open(OBSIDIAN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Obsidian обновлён: {updated_at}")
    print(f"   Заявок: {total_bookings} | Последняя: {last_date}")
    print(f"   Фото в очереди: {photos_count} | Видео готово: {videos_count}")


if __name__ == "__main__":
    sync()
