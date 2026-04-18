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
- [x] Procfile: `web: python main.py` — Railway открывает публичный порт
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
- [x] Fallback OWNER_CHAT_ID = 1914219730 (если не задан в env)
- [x] CORS для dzbbot-spec.github.io и shale-relax.netlify.app
- [x] OPTIONS preflight handler

### Мини-апп (React + Vite + TypeScript)
- [x] 4 страницы: Главная, Галерея, О домиках, Заявка
- [x] Нижняя навигация iOS-стиль: белая панель + blur + иконки + подписи
- [x] Слайдер на главной: свайп пальцем (порог 50px), без автопрокрутки
- [x] Форма бронирования: валидация, подсчёт стоимости ночей
- [x] Поля ввода: фокус-стиль (#111), scrollIntoView при фокусе
- [x] Кнопки ±  счётчика гостей с press-эффектом (150ms)
- [x] Мобильная вёрстка: 44px inputs, 16px отступы, safe-area-inset-bottom
- [x] iOS: fontSize 16px на всех input/textarea — предотвращает автозум
- [x] iOS: `maximum-scale=1` в viewport meta — запрет зума
- [x] Поля дат: `type="date"` с `-webkit-appearance: none`, без JS-трюков
- [x] Страница «О домиках»: текстовые блоки без фото (характеристики + инфоблоки)
- [x] Фото из Cloudinary (q_auto,f_auto,w_800), lazy loading, fetchpriority на 1-й слайд
- [x] 24 фото загружены в Cloudinary (9 exterior + 14 interior)

### Деплой мини-аппа
- [x] GitHub Pages: dzbbot-spec.github.io/shale-relax
- [x] GitHub Actions workflow: автодеплой при пуше в main (только `mini-app/**`)
- [x] Vite base path: `/shale-relax/` в GitHub Actions окружении
- [x] VITE_API_URL: worker-production-8fd9.up.railway.app

### ИИ-конвейер (код готов, не протестирован с реальными ключами)
- [x] `kling.py` — генерация видео через Kling AI (JWT-аутентификация)
- [x] `gpt.py` — подписи через OpenAI + фильтр запрещённых слов (ФЗ-72)
- [x] `smmbox.py` — публикация через Smmbox API
- [x] `pipeline.py` — оркестратор конвейера
- [x] APScheduler: пн-вс 10:00, 11:00, 12:00 МСК

---

## 🔜 Следующие шаги

### Шаг 1 — Протестировать мини-апп в Telegram
- [ ] Открыть @shale_relax_bot → кнопка «🌐 Витрина»
- [ ] Проверить свайп слайдера на iPhone
- [ ] Заполнить форму → убедиться что заявка дошла в Telegram владельцу

### Шаг 2 — Тест ИИ-конвейера
- [ ] Положить 1 фото в `data/photos/`
- [ ] Запустить: `python -m pipeline.pipeline`
- [ ] Проверить: видео в `ready_to_post/`, уведомление в Telegram

### Шаг 3 — Управляющий
- [ ] Узнать chat_id управляющего через @userinfobot
- [ ] Добавить `MANAGER_CHAT_ID` в Railway env vars

### Шаг 4 — Smmbox (автопубликация в Instagram)
- [ ] Оплатить тариф на smmbox.com (1700 руб/мес)
- [ ] Подключить Instagram @shale_relax_elbrus
- [ ] Добавить `SMMBOX_API_KEY`, `SMMBOX_ACCOUNT_ID` в Railway env

### Шаг 5 — Railway: продлить или перенести на VPS
- [ ] До ~11 мая 2026 решить: оплатить Railway (~500 руб/мес) или перенести на VPS
- [ ] При переносе на VPS: systemd-сервис, обновить MINI_APP_URL в боте

---

## 📋 Доступы и ключи

| Сервис | Статус |
|--------|--------|
| Telegram Bot Token | ✅ Активен |
| OpenAI API Key | ⚠️ Нет баланса — пополнить $5 |
| Kling Access + Secret Key | ✅ Настроены |
| Cloudinary (dfbhw1rfx) | ✅ 24 фото загружены |
| GitHub PAT (repo + workflow scope) | ✅ Активен |
| MANAGER_CHAT_ID | ❌ Не задан |
| Smmbox | ❌ Нет тарифа |

---

## 🏗 Архитектура

```
shale-relax/
├── main.py                      # Точка входа: бот + HTTP API + планировщик
├── bot/
│   ├── handlers.py              # FSM бронирование + FAQ + приём фото
│   └── keyboard.py              # Меню + кнопка мини-аппа (MINI_APP_URL из env)
├── pipeline/
│   ├── pipeline.py              # Оркестратор
│   ├── kling.py                 # Генерация видео (Kling AI)
│   ├── gpt.py                   # Генерация подписей (OpenAI)
│   └── smmbox.py                # Публикация (Smmbox)
├── mini-app/                    # React мини-апп → GitHub Pages
│   ├── index.html               # viewport maximum-scale=1 (iOS no-zoom)
│   └── src/
│       ├── pages/
│       │   ├── Home.tsx         # Слайдер со свайпом, теги, кнопки
│       │   ├── GalleryPage.tsx  # Галерея exterior/interior + лайтбокс
│       │   ├── Chalet.tsx       # Характеристики + инфоблоки (без фото)
│       │   └── Booking.tsx      # Форма заявки → POST /api/booking
│       ├── components/
│       │   └── NavBar.tsx       # iOS-стиль: blur, иконки, подписи
│       └── config/
│           └── photos.ts        # Cloudinary URLs (q_auto,f_auto,w_800)
├── .github/workflows/
│   └── deploy-mini-app.yml      # Автодеплой на GitHub Pages
├── Procfile                     # web: python main.py
└── railway.toml                 # startCommand + restartPolicy
```

## 🐛 Решённые проблемы

| Проблема | Решение |
|----------|---------|
| Railway 404 "Application not found" | Procfile `worker:` → `web:` |
| GitHub Pages не деплоился | Репо было приватным → сделали публичным, включили Pages через API |
| Билд падал на CI | `const today` объявлен но не использовался — удалён |
| iOS автозум при вводе | fontSize 16px + maximum-scale=1 в viewport |
| Поля дат обрезались | Убран grid, каждое поле на отдельной строке, `type="date"` напрямую |
| Неверный Railway URL в коде | shale-relax-production → worker-production-8fd9 |
| CORS блокировал запросы | Добавлен github.io в ALLOWED_ORIGINS |
