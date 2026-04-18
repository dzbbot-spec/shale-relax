# ТЕХНИЧЕСКОЕ ЗАДАНИЕ — Шале Релакс
**Версия:** 3.0  
**Дата:** 18 апреля 2026  
**Статус:** В работе — мини-апп задеплоен, бот работает

---

## Паспорт проекта

| Параметр | Значение |
|----------|----------|
| Название | Шале Релакс |
| Описание | Автономная система привлечения клиентов для аренды домиков у Эльбруса |
| Цель | Привлекать клиентов (15 000 руб./сутки) с минимальным участием владельца |
| Участие владельца | Отправка фото раз в неделю + ответы на готовые заявки |

---

## 1. Объект

- **Название:** Шале Релакс
- **Количество домиков:** 2 (одинаковые)
- **Расположение:** пос. Эльбрус, Кабардино-Балкария, 1800 м н.у.м.
- **Цена:** 15 000 руб./сутки
- **Особенности:** тихий конец посёлка, вид на горы, 5 минут пешком до подъёмников Эльбруса и Чегета

**Оснащение каждого домика:**
- 2 спальни (двуспальные кровати)
- до 6 гостей
- Кухня с посудой и техникой
- Тёплый пол
- Телевизор (Smart TV)
- Wi-Fi
- Мангал и костровая зона
- Бесплатная парковка

**Заселение:** самозаезд по коду, заезд с 14:00, выезд до 12:00, залог при заселении.

---

## 2. Регистрационные данные

> Чувствительные данные (токены, ключи, пароли) хранятся в `.env` и в Bitwarden.

| Сервис | Логин / Аккаунт | Примечание |
|--------|----------------|------------|
| Gmail | dzb.bot@gmail.com | Рабочий аккаунт проекта |
| Telegram Bot | @shale_relax_bot | Токен: `8746481373:AAEpwwQqSH_s_e38yhCvNcPIEKCdo4bNmC8` |
| Telegram владельца | @shale_relax_elbrus | chat_id: `1914219730` |
| Instagram | @shale_relax_elbrus | Логин: dzablaev@gmail.com |
| OpenAI | — | API Key в `.env` |
| Kling AI | — | Access: `A4dCQDh8yFARG4agTkpMCEFRLpyTCbmg` / Secret: `TLCfdRR83eHb3QeaPPmRNK3frLBGhyGR` |
| Cloudinary | dfbhw1rfx | api_key: `957944298884622` |
| GitHub | dzbbot-spec | Репо: dzbbot-spec/shale-relax (публичный) |
| Railway | — | worker-production-8fd9.up.railway.app |
| GitHub Pages | — | dzbbot-spec.github.io/shale-relax |
| Smmbox | dzb.bot@gmail.com | Тариф не оплачен |
| Bitwarden | — | Хранилище всех паролей |

---

## 3. Архитектура системы

```
Фото от управляющего
        ↓
  Telegram-бот (@shale_relax_bot)
        ↓
  ИИ-конвейер (Railway)
    ├── Kling AI → видео из фото
    ├── OpenAI GPT → атмосферная подпись
    └── Smmbox → публикация в Instagram
        ↓
  Instagram (@shale_relax_elbrus)
        ↓
  Клиент → Telegram-бот → заявка → владелец
```

**Мини-апп (Telegram WebApp):**
```
Telegram-бот → кнопка «Витрина» → GitHub Pages (мини-апп)
                                         ↓
                              Форма заявки → Railway API → владелец
```

---

## 4. Компоненты системы

### 4.1 Telegram-бот (aiogram 3.x, Railway)

**Файлы:**
- `main.py` — точка входа: бот + HTTP-сервер (aiohttp) + планировщик (APScheduler)
- `bot/handlers.py` — FSM-сценарий бронирования + FAQ + приём фото
- `bot/keyboard.py` — главное меню + кнопка мини-аппа

**Сценарий бронирования (FSM):**
1. Имя
2. Даты поездки
3. Количество гостей
4. Контакт (телефон или @username)
→ Заявка пересылается владельцу в Telegram + сохраняется в `data/bookings.json`

**FAQ кнопки:**
- Как добраться
- Что посмотреть
- Эндуро-маршруты
- Трансфер
- Наши домики

**Приём фото от управляющего:**
- Управляющий присылает фото в бот
- Бот сохраняет в `data/photos/` для конвейера

### 4.2 HTTP API (aiohttp, тот же процесс)

- `GET /` — health check для Railway
- `POST /api/booking` — приём заявок из мини-аппа
  - Входные данные: `{name, check_in, check_out, guests, contact, comment}`
  - Форматирует и пересылает владельцу через бота
  - CORS: dzbbot-spec.github.io, shale-relax.netlify.app
- `OPTIONS /api/booking` — preflight

### 4.3 ИИ-конвейер (pipeline/)

**Поток:**
1. Фото из `data/photos/`
2. `kling.py` — отправка в Kling AI, получение видео
3. `gpt.py` — генерация подписи по рубрике дня
4. `smmbox.py` — скачивание видео + публикация через Smmbox API

**Расписание (APScheduler):** пн-вс 10:00, 11:00, 12:00 МСК

**Рубрики по дням:**
| День | Рубрика | Хэштеги |
|------|---------|---------|
| Пн | Природа и виды | #Эльбрус #горы |
| Вт | Жизнь домиков | #ШалеРелакс #уютныйдом |
| Ср | Активности | #эндуро #лыжи #Чегет |
| Чт | Партнёры и инфра | #Приэльбрусье #термальные |
| Пт | Атмосфера вечера | #горнаяатмосфера #вечер |
| Сб | Выходной контент | #отдых #горы #weekend |
| Вс | Итоги / UGC | #Кабардино #природа |

**Правило GPT:** запрещены слова «аренда», «бронирование», «цена», «стоимость», «заказать», «купить» (ФЗ-72).

### 4.4 Мини-апп (React + Vite + TypeScript)

**URL:** https://dzbbot-spec.github.io/shale-relax  
**Деплой:** GitHub Actions при пуше в main (только `mini-app/**`)

**Страницы:**
1. **Главная** — слайдер exterior-фото (свайп, без автопрокрутки), теги, кнопки «Подробнее» / «Забронировать»
2. **Галерея** — вкладки exterior/interior, 2-колоночная сетка, лайтбокс
3. **О домиках** — характеристики 2×4, текстовые инфоблоки (расположение, вид, заселение, правила)
4. **Заявка** — форма → POST /api/booking → Railway

**Дизайн:**
- Минималистичный: белый фон `#ffffff`, чёрный текст `#111111`
- Без эмодзи в UI
- Навигация: iOS-стиль, фиксированная панель снизу, белый фон + `backdrop-filter: blur(20px)`, граница `0.5px solid rgba(0,0,0,0.1)`
- Кнопки: `borderRadius: 12px`, `fontSize: 14px`
- Карточки: `borderRadius: 12px`, фон `#f5f5f5`

**Мобильные требования:**
- `font-size: 16px` на всех input (предотвращает zoom на iOS)
- `maximum-scale=1` в viewport meta
- `type="date"` с `-webkit-appearance: none`
- `safe-area-inset-bottom` в paddingBottom
- `scrollIntoView` при фокусе на поле

**Фото:**
- 9 exterior + 14 interior загружены в Cloudinary
- URL: `https://res.cloudinary.com/dfbhw1rfx/image/upload/q_auto,f_auto,w_800/shale-relax/...`
- Первый слайд: `fetchpriority="high"`, остальные: `loading="lazy"`

---

## 5. Стек технологий

| Компонент | Технология | Хостинг |
|-----------|-----------|---------|
| Бот + API | Python 3.x, aiogram 3.x, aiohttp, APScheduler | Railway |
| Мини-апп | React 19, Vite, TypeScript, Tailwind CSS v4 | GitHub Pages |
| Фото | Cloudinary (CDN + трансформации) | Cloud |
| Видео из фото | Kling AI (kling-v1-5) | API |
| Подписи | OpenAI GPT (gpt-4o-mini) | API |
| Автопостинг | Smmbox.com | SaaS |
| CI/CD | GitHub Actions | GitHub |
| Хранилище паролей | Bitwarden | Cloud |

---

## 6. Переменные окружения (.env / Railway)

```env
# Telegram
TELEGRAM_BOT_TOKEN=8746481373:AAEpwwQqSH_s_e38yhCvNcPIEKCdo4bNmC8
OWNER_CHAT_ID=1914219730
MINI_APP_URL=https://dzbbot-spec.github.io/shale-relax

# OpenAI
OPENAI_API_KEY=sk-proj-...

# Kling AI
KLING_ACCESS_KEY=A4dCQDh8yFARG4agTkpMCEFRLpyTCbmg
KLING_SECRET_KEY=TLCfdRR83eHb3QeaPPmRNK3frLBGhyGR
KLING_MODEL=kling-v1-5

# Smmbox (не заполнен)
SMMBOX_API_KEY=
SMMBOX_ACCOUNT_ID=

# Управляющий (не заполнен)
MANAGER_CHAT_ID=

# Прочее
LOG_LEVEL=INFO
TIMEZONE=Europe/Moscow
DOWNLOAD_PATH=./downloads
LOGS_PATH=./logs
```

---

## 7. Инфраструктура

| Параметр | Значение |
|----------|----------|
| Railway URL | worker-production-8fd9.up.railway.app |
| Railway порт | 8080 (из env PORT) |
| Procfile | `web: python main.py` |
| GitHub Pages | dzbbot-spec.github.io/shale-relax |
| Vite base | `/shale-relax/` (в GitHub Actions) |

---

## 8. Статус сервисов (на 18.04.2026)

| Сервис | Статус | Стоимость | Срок |
|--------|--------|-----------|------|
| Railway | ✅ Работает | ~500 руб/мес | Триал до ~11 мая 2026 |
| GitHub Pages | ✅ Работает | Бесплатно | — |
| Cloudinary | ✅ Работает | Бесплатно | Free tier |
| Telegram Bot | ✅ Работает | Бесплатно | — |
| OpenAI API | ⚠️ Нет баланса | ~300–600 руб/мес | Пополнить $5 |
| Kling AI | ⚠️ Нет баланса | ~700–1800 руб/мес | Пополнить |
| Smmbox | ❌ Не подключён | 1700 руб/мес | После оплаты |

---

## 9. Следующие шаги

### Срочно (апрель 2026)
- [ ] Протестировать форму бронирования end-to-end в Telegram на iPhone
- [ ] Оплатить Railway до ~11 мая (или перенести на VPS ~500 руб/мес)
- [ ] Пополнить OpenAI API (минимум $5)

### Конвейер (после пополнения ключей)
- [ ] Получить chat_id управляющего → добавить `MANAGER_CHAT_ID` в Railway
- [ ] Положить 1 фото в `data/photos/`, запустить `python -m pipeline.pipeline`
- [ ] Убедиться: видео в `ready_to_post/`, уведомление владельцу

### Instagram-автоматизация (этап 2)
- [ ] Оплатить Smmbox (1700 руб/мес)
- [ ] Подключить @shale_relax_elbrus к Smmbox
- [ ] Добавить `SMMBOX_API_KEY` в Railway env
- [ ] Запустить первую публикацию

---

## 10. Юридические требования (ФЗ-72)

С сентября 2025 года реклама в Instagram запрещена. Правила:
- Instagram: **только атмосферный контент** — природа, интерьер, активности
- Запрещены слова: аренда, бронирование, цена, стоимость, заказать, купить
- Все продающие элементы — только в Telegram-боте и мини-аппе

---

## 11. Структура репозитория

```
shale-relax/
├── main.py                      # Точка входа
├── bot/
│   ├── handlers.py              # FSM + FAQ
│   └── keyboard.py              # Меню бота
├── pipeline/
│   ├── pipeline.py              # Оркестратор
│   ├── kling.py                 # Kling AI
│   ├── gpt.py                   # OpenAI
│   └── smmbox.py                # Smmbox
├── utils/
│   ├── helpers.py               # Форматирование заявок
│   ├── logger.py                # Логирование
│   └── obsidian_sync.py         # Синхронизация с Obsidian
├── prompts/
│   ├── system_prompt_gpt.txt    # Промпт для GPT
│   └── kling_prompts.json       # 12 промптов по рубрикам
├── mini-app/                    # React мини-апп
│   ├── index.html               # viewport maximum-scale=1
│   └── src/
│       ├── pages/
│       │   ├── Home.tsx         # Слайдер, теги, кнопки
│       │   ├── GalleryPage.tsx  # Галерея + лайтбокс
│       │   ├── Chalet.tsx       # О домиках (без фото)
│       │   └── Booking.tsx      # Форма заявки
│       ├── components/
│       │   └── NavBar.tsx       # iOS-навигация
│       └── config/
│           └── photos.ts        # Cloudinary URLs
├── .github/workflows/
│   └── deploy-mini-app.yml      # CI/CD → GitHub Pages
├── data/
│   ├── bookings.json            # Заявки
│   └── photos/                  # Фото от управляющего
├── Procfile                     # web: python main.py
├── railway.toml                 # Railway конфиг
├── requirements.txt             # Python зависимости
└── .env                         # Ключи (не в git)
```
