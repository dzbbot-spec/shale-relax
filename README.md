# Шале Релакс — Автоматизация

Автономная система привлечения клиентов для аренды домиков у подножия Эльбруса.

- **Instagram:** @shale_relax_elbrus
- **Telegram-бот:** @shale_relax_bot

## Что делает система

| Компонент | Роль |
|-----------|------|
| `main.py` | Telegram-бот: приём заявок, FAQ, пересылка владельцу |
| `pipeline/pipeline.py` | ИИ-конвейер: фото → видео (Kling) → подпись (GPT) → публикация (Smmbox) |
| `scheduler.py` | Автозапуск конвейера по расписанию (пн-вс, 10:00-12:00 МСК) |

## Установка

```bash
# 1. Клонируйте репозиторий и перейдите в папку
cd shale-relax

# 2. Создайте виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Создайте .env из шаблона
cp .env.example .env
# Откройте .env и заполните все поля
```

## Конфигурация `.env`

| Переменная | Обязательна | Описание |
|------------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Токен от @BotFather |
| `OWNER_CHAT_ID` | ✅ | Chat ID для пересылки заявок |
| `OPENAI_API_KEY` | ✅ | Ключ OpenAI для подписей |
| `UMNIK_KLING_API_KEY` | Для конвейера | Ключ Kling AI (umnik.ai) |
| `SMMBOX_API_KEY` | Для конвейера | Ключ Smmbox для публикации |
| `SMMBOX_ACCOUNT_ID` | Для конвейера | ID Instagram-аккаунта в Smmbox |
| `MANAGER_CHAT_ID` | Рекомендуется | Chat ID управляющего |

## Запуск

### Telegram-бот

```bash
python main.py
```

### Разовый запуск конвейера вручную

```bash
python -m pipeline.pipeline
```

### Планировщик (автозапуск конвейера по расписанию)

```bash
python scheduler.py
```

### Совместный запуск бота и планировщика

Рекомендуется запускать как два отдельных процесса (например, через `screen` или `systemd` на VPS):

```bash
# Терминал 1
python main.py

# Терминал 2
python scheduler.py
```

## Как работает конвейер

1. Управляющий отправляет фото боту в Telegram
2. Фото сохраняются в `data/photos/`
3. По расписанию (или вручную) запускается `pipeline.py`:
   - Kling AI генерирует видео из фото
   - GPT пишет атмосферную подпись (без запрещённых слов)
   - Smmbox публикует рилс в Instagram
4. Обработанное фото перемещается в `data/photos/processed/`

## Структура проекта

```
shale-relax/
├── main.py                  # Запуск бота
├── scheduler.py             # Планировщик
├── config.py                # Централизованная конфигурация
├── bot/
│   ├── handlers.py          # Обработчики aiogram 3.x
│   └── keyboard.py          # Клавиатуры
├── pipeline/
│   ├── pipeline.py          # Оркестратор конвейера
│   ├── kling.py             # Клиент Kling AI
│   ├── gpt.py               # Клиент OpenAI
│   └── smmbox.py            # Клиент Smmbox
├── utils/
│   ├── logger.py            # Логирование
│   └── helpers.py           # Retry и хелперы
├── prompts/
│   ├── system_prompt_gpt.txt  # Системный промпт GPT
│   └── kling_prompts.json     # Библиотека промптов Kling
├── data/
│   ├── photos/              # Очередь входящих фото
│   └── bookings.json        # Архив заявок
├── logs/                    # Файлы логов
├── .env                     # Реальные ключи (в git не попадает)
├── .env.example             # Шаблон конфигурации
└── requirements.txt
```

## Логи

Все логи пишутся в консоль и в файлы:
- `logs/bot.log` — события бота
- `logs/pipeline.log` — конвейер
- `logs/scheduler.log` — планировщик

## Деплой на VPS

```bash
# Установка зависимостей на сервере (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-venv python3-pip -y

# Клонирование и настройка
git clone <repo> shale-relax && cd shale-relax
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env

# Запуск через screen (для продакшена рекомендуется systemd)
screen -S shale-bot -dm python main.py
screen -S shale-scheduler -dm python scheduler.py
```
