# Шале Релакс — контекст для Claude Code

## Что это за проект

Автоматизированная система привлечения клиентов для аренды 2 домиков у подножия Эльбруса (пос. Эльбрус, КБР, 1800м, 15 000 руб/сутки). Владелец — @shale_relax_elbrus, chat_id 1914219730.

Система состоит из:
- **Telegram-бота** (@shale_relax_bot) — FAQ, FSM-бронирование, приём фото от управляющего
- **HTTP API** (aiohttp) — `POST /api/booking` для мини-аппа
- **Мини-аппа** (React + Vite → GitHub Pages) — витрина + форма заявки
- **ИИ-конвейера** (Kling AI + GPT + Smmbox) — фото → видео → Instagram

## Ключевые URL и данные

| Параметр | Значение |
|----------|----------|
| Railway (бот + API) | worker-production-8fd9.up.railway.app |
| Мини-апп | dzbbot-spec.github.io/shale-relax |
| GitHub | github.com/dzbbot-spec/shale-relax (публичный) |
| Cloudinary | dfbhw1rfx, фото: q_auto,f_auto,w_800 |
| OWNER_CHAT_ID | 1914219730 |
| Telegram Bot | @shale_relax_bot |
| Телефон | +7 928 910-76-01 |
| Instagram | @shale_relax_elbrus |
| Координаты домиков | 43.251272, 42.636834 |
| GitHub PAT | в Bitwarden (repo + workflow scope) |

## Текущий статус (19 апреля 2026)

- ✅ Бот работает на Railway
- ✅ Мини-апп на GitHub Pages (6 экранов: Главная, Галерея, О домиках, Вокруг нас, Заявка, Контакты)
- ✅ Экран «Контакты» — телефон, Telegram, Instagram, адрес, карта
- ✅ Экран «Вокруг нас» — активности и маршруты
- ✅ Лайтбокс в галерее — свайп и стрелки
- ✅ FAQ в разделе «О домиках»
- ✅ Карта Leaflet с координатами домиков (43.251272, 42.636834)
- ✅ 24 фото в Cloudinary (9 exterior + 14 interior)
- ✅ iOS-фиксы: fontSize 16px, maximum-scale=1
- ⚠️ OpenAI API — нет баланса (нужно $5)
- ⚠️ Kling AI — нет баланса
- ❌ Smmbox — тариф не оплачен (1700 руб/мес)
- ❌ MANAGER_CHAT_ID — не задан
- ⚠️ Railway — триал до ~11 мая 2026

## Объект

- 2 одинаковых домика, пос. Эльбрус, КБР
- 2 спальни, до 6 гостей, кухня, тёплый пол, TV, Wi-Fi, мангал, парковка
- Цена: 15 000 руб/сутки
- Координаты: 43.251272, 42.636834
- Телефон: +7 928 910-76-01

## Стек

- **Бот:** Python 3, aiogram 3.x, aiohttp, APScheduler
- **Мини-апп:** React 19, Vite, TypeScript, Tailwind CSS v4, Leaflet.js
- **Деплой:** Railway (бот), GitHub Pages (мини-апп), GitHub Actions (CI/CD)
- **Фото:** Cloudinary CDN
- **ИИ:** Kling AI (видео), OpenAI gpt-4o-mini (подписи), Smmbox (постинг)

## Структура мини-аппа (6 экранов)

```
mini-app/src/pages/
├── Home.tsx        # Слайдер (свайп), теги, атмосферное описание
├── GalleryPage.tsx # Галерея exterior/interior + лайтбокс со свайпом
├── Chalet.tsx      # Удобства + инфоблоки + FAQ
├── Around.tsx      # Вокруг нас — активности и маршруты
├── Booking.tsx     # Форма заявки → POST /api/booking
└── Contacts.tsx    # Телефон, Telegram, Instagram, адрес, карта Leaflet
```

## Правила работы

- Commit-сообщения на английском: `feat:`, `fix:`, `docs:`, `chore:`
- После изменений в mini-app — пушить, Actions задеплоит сам
- `font-size: 16px` на всех input — iOS не зумит
- `maximum-scale=1` в viewport
- `safe-area-inset-bottom` в paddingBottom страниц и NavBar
- Cloudinary URL с `q_auto,f_auto,w_800`
- Railway домен: `worker-production-8fd9.up.railway.app`
- Procfile: `web: python main.py`
- CORS разрешён для `dzbbot-spec.github.io`

## Нерешённые задачи (следующие шаги)

- [ ] Оплатить Railway до ~11 мая
- [ ] Пополнить OpenAI ($5) и Kling AI
- [ ] Узнать MANAGER_CHAT_ID управляющего
- [ ] Снять фото домиков №1 и №2 отдельно
- [ ] Придумать названия домиков
- [ ] Добавить отзывы гостей
- [ ] Протестировать ИИ-конвейер
- [ ] Подключить Smmbox

## Решённые проблемы

| Проблема | Решение |
|----------|---------|
| Railway 404 | Procfile `worker:` → `web:` |
| GitHub Pages 404 | Репо публичный |
| iOS зумит при вводе | font-size 16px + maximum-scale=1 |
| Поля дат обрезались | Поля вертикально, без grid |
| Фото не грузились | .gitignore исправлен |
| Netlify лимит | Переехали на GitHub Pages |
| CORS ошибки | github.io добавлен в ALLOWED_ORIGINS |
