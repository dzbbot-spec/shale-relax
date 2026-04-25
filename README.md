# Шале Релакс

Система привлечения клиентов для аренды 2 домиков у подножия Эльбруса (пос. Эльбрус, КБР).

- **Мини-апп:** [dzbbot-spec.github.io/shale-relax](https://dzbbot-spec.github.io/shale-relax)
- **Telegram-бот:** [@shale_relax_bot](https://t.me/shale_relax_bot)
- **Instagram:** [@shale_relax_elbrus](https://instagram.com/shale_relax_elbrus)

## Архитектура

| Компонент | Описание | Деплой |
|-----------|----------|--------|
| `main.py` | Telegram-бот: FAQ, FSM-бронирование, приём фото от управляющего | Railway |
| `bot/` | Хэндлеры aiogram 3.x, клавиатуры | — |
| `pipeline/` | ИИ-конвейер: фото → видео (Kling) → подпись (GPT) → Instagram (Smmbox) | вручную |
| `mini-app/` | React-витрина: 6 экранов, форма заявки | GitHub Pages |

## Мини-апп (React + Vite + TypeScript)

6 экранов, деплой через GitHub Actions на GitHub Pages:

```
mini-app/src/pages/
├── Home.tsx        # Слайдер, теги, описание
├── GalleryPage.tsx # Галерея exterior/interior, лайтбокс со свайпом
├── Chalet.tsx      # Удобства, инфоблоки, FAQ
├── Around.tsx      # Вокруг нас: курорты, природа, активности
├── Booking.tsx     # Форма заявки → POST /api/booking
└── Contacts.tsx    # Телефон, Telegram, Instagram, карта Leaflet
```

Фото хранятся в Cloudinary CDN (`shale-relax/exterior/` и `shale-relax/interior/`).

## Установка

```bash
# Python-зависимости (бот + API)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # заполнить ключи

# Мини-апп (локально)
cd mini-app && npm install && npm run dev
```

## Конфигурация `.env`

| Переменная | Описание |
|------------|----------|
| `TELEGRAM_BOT_TOKEN` | Токен от @BotFather |
| `OWNER_CHAT_ID` | Chat ID для пересылки заявок (1914219730) |
| `OPENAI_API_KEY` | OpenAI для подписей к видео |
| `KLING_ACCESS_KEY` / `KLING_SECRET_KEY` | Kling AI для генерации видео |
| `SMMBOX_API_KEY` / `SMMBOX_ACCOUNT_ID` | Smmbox для публикации в Instagram |
| `MANAGER_CHAT_ID` | Chat ID управляющего (опционально) |

## Запуск

```bash
# Бот + HTTP API (Railway запускает автоматически)
python main.py

# ИИ-конвейер вручную
python -m pipeline.pipeline
```

## Структура проекта

```
shale-relax/
├── main.py              # Точка входа: бот + aiohttp API
├── config.py            # Централизованная конфигурация
├── Procfile             # Railway: web: python main.py
├── bot/
│   ├── handlers.py      # Обработчики aiogram 3.x
│   └── keyboard.py      # Клавиатуры
├── pipeline/
│   ├── pipeline.py      # Оркестратор конвейера
│   ├── kling.py         # Клиент Kling AI
│   ├── gpt.py           # Клиент OpenAI
│   └── smmbox.py        # Клиент Smmbox
├── utils/
│   ├── logger.py        # Логирование
│   └── helpers.py       # Retry и хелперы
├── prompts/             # Промпты для GPT и Kling
├── mini-app/            # React-мини-апп
├── data/                # bookings.json, очередь фото
├── .env.example         # Шаблон конфигурации
└── requirements.txt
```

## Деплой

- **Бот + API:** Railway (`worker-production-8fd9.up.railway.app`), автодеплой при пуше в `main`
- **Мини-апп:** GitHub Pages, GitHub Actions деплоит при изменениях в `mini-app/**`

## Логи

- `logs/bot.log` — события бота
- `logs/pipeline.log` — ИИ-конвейер
