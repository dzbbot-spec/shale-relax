# PROGRESS.md — Шале Релакс

## Статус: 🟢 Бот + Мини-апп работают

Последнее обновление: **18 апреля 2026**

---

## ✅ Готово

### Инфраструктура
- [x] Структура проекта (`bot/`, `pipeline/`, `utils/`, `prompts/`)
- [x] `.env` заполнен ключами (Telegram, OpenAI, Kling, Cloudinary)
- [x] `requirements.txt` — aiogram 3.x + aiohttp + pydantic-settings
- [x] `.gitignore` — `.env` и медиафайлы защищены
- [x] Деплой на Railway (worker-production-8fd9.up.railway.app)
- [x] GitHub репозиторий публичный (dzbbot-spec/shale-relax)

### Telegram-бот
- [x] FSM-сценарий бронирования: имя → даты → гости → контакт
- [x] Заявка пересылается владельцу (OWNER_CHAT_ID=1914219730)
- [x] Заявка сохраняется в `data/bookings.json`
- [x] FAQ: как добраться, что посмотреть, эндуро, трансфер, домики
- [x] Приём фото от управляющего → `data/photos/`
- [x] Кнопка «🌐 Витрина» открывает мини-апп

### HTTP API
- [x] `POST /api/booking` на aiohttp (параллельно с ботом)
- [x] Принимает JSON: name, check_in, check_out, guests, contact, comment
- [x] Пересылает заявку владельцу через бота
- [x] CORS для dzbbot-spec.github.io и shale-relax.netlify.app
- [x] Fallback OWNER_CHAT_ID = 1914219730
- [x] Procfile: `web: python main.py` (Railway открывает порт)

### Мини-апп (React + Vite + TypeScript)
- [x] 4 страницы: Главная, Галерея, О домиках, Заявка
- [x] Нижняя навигация iOS-стиль (белая панель, blur, иконки + подписи)
- [x] Слайдер на главной: свайп пальцем, без автопрокрутки
- [x] Форма бронирования с валидацией и подсчётом стоимости
- [x] Поля ввода: фокус-стиль, placeholder, scrollIntoView при фокусе
- [x] Кнопки счётчика гостей с press-эффектом
- [x] Мобильная вёрстка: 44px inputs, 16px отступы, safe-area
- [x] Фото из Cloudinary (q_auto,f_auto,w_800), lazy loading
- [x] 24 фото загружены в Cloudinary (9 exterior + 14 interior)

### Деплой мини-аппа
- [x] GitHub Pages: dzbbot-spec.github.io/shale-relax
- [x] GitHub Actions workflow: автодеплой при пуше в main
- [x] Vite base path: `/shale-relax/` в GitHub Actions окружении
- [x] VITE_API_URL: worker-production-8fd9.up.railway.app

### ИИ-конвейер (код готов, не протестирован с реальными ключами)
- [x] `kling.py` — генерация видео через Kling AI
- [x] `gpt.py` — подписи через OpenAI + фильтр запрещённых слов
- [x] `smmbox.py` — публикация через Smmbox
- [x] `pipeline.py` — оркестратор
- [x] APScheduler: пн-вс 10:00, 11:00, 12:00 МСК

---

## 🔜 Следующие шаги

### Шаг 1 — Проверить мини-апп в Telegram
- [ ] Открыть @shale_relax_bot → кнопка «🌐 Витрина»
- [ ] Проверить свайп слайдера
- [ ] Заполнить форму → убедиться что заявка дошла в Telegram

### Шаг 2 — Тест конвейера
- [ ] Положить 1 фото в `data/photos/`
- [ ] Запустить: `python -m pipeline.pipeline`
- [ ] Проверить: видео в `ready_to_post/`, уведомление в Telegram

### Шаг 3 — Управляющий
- [ ] Узнать chat_id управляющего через @userinfobot
- [ ] Добавить `MANAGER_CHAT_ID` в Railway env vars

### Шаг 4 — Smmbox (автопубликация)
- [ ] Оплатить тариф на smmbox.com (1700 руб/мес)
- [ ] Добавить `SMMBOX_API_KEY`, `SMMBOX_ACCOUNT_ID` в Railway env

### Шаг 5 — Railway → продление или VPS
- [ ] До ~11 мая 2026 решить: оплатить Railway (~500 руб/мес) или перенести на VPS
- [ ] При переносе: настроить systemd-сервис, обновить MINI_APP_URL в боте

---

## 📋 Доступы и ключи

| Сервис | Статус |
|--------|--------|
| Telegram Bot Token | ✅ Активен |
| OpenAI API Key | ⚠️ Нет баланса — пополнить $5 |
| Kling Access + Secret Key | ✅ Настроены |
| Cloudinary (dfbhw1rfx) | ✅ 24 фото загружены |
| GitHub PAT (workflow scope) | ✅ Активен |
| MANAGER_CHAT_ID | ❌ Не задан |
| Smmbox | ❌ Нет тарифа |

---

## 🏗 Архитектура

```
shale-relax/
├── main.py              # Точка входа: бот + HTTP API + планировщик
├── bot/
│   ├── handlers.py      # FSM бронирование + FAQ
│   └── keyboard.py      # Меню + кнопка мини-аппа
├── pipeline/
│   ├── pipeline.py      # Оркестратор
│   ├── kling.py         # Генерация видео
│   ├── gpt.py           # Генерация подписей
│   └── smmbox.py        # Публикация
├── mini-app/            # React мини-апп → GitHub Pages
│   └── src/
│       ├── pages/       # Home, Gallery, Chalet, Booking
│       ├── components/  # NavBar
│       └── config/      # photos.ts (Cloudinary URLs)
├── .github/workflows/
│   └── deploy-mini-app.yml  # Автодеплой на GitHub Pages
├── Procfile             # web: python main.py
└── railway.toml         # Railway конфигурация
```
