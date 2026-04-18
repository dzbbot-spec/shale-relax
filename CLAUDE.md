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
| GitHub PAT | в Bitwarden (repo + workflow scope) |

## Текущий статус (18 апреля 2026)

- ✅ Бот работает на Railway
- ✅ Мини-апп задеплоен на GitHub Pages, автодеплой через Actions
- ✅ `POST /api/booking` принимает заявки из мини-аппа и пересылает владельцу
- ✅ 24 фото загружены в Cloudinary (9 exterior + 14 interior)
- ✅ iOS-фиксы: fontSize 16px, maximum-scale=1, type="date" напрямую
- ⚠️ OpenAI API — нет баланса (нужно $5)
- ⚠️ Kling AI — нет баланса
- ❌ Smmbox — тариф не оплачен (1700 руб/мес)
- ⚠️ Railway — триал до ~11 мая 2026

## Стек

- **Бот:** Python 3, aiogram 3.x, aiohttp, APScheduler, pydantic-settings
- **Мини-апп:** React 19, Vite, TypeScript, Tailwind CSS v4
- **Деплой:** Railway (бот), GitHub Pages (мини-апп), GitHub Actions (CI/CD)
- **Фото:** Cloudinary CDN
- **ИИ:** Kling AI (видео), OpenAI gpt-4o-mini (подписи), Smmbox (постинг)

## Структура репозитория

```
main.py                    # Точка входа: бот + aiohttp + APScheduler
bot/handlers.py            # FSM бронирование + FAQ + приём фото
bot/keyboard.py            # Меню + WebApp кнопка (MINI_APP_URL из env)
pipeline/                  # kling.py, gpt.py, smmbox.py, pipeline.py
utils/obsidian_sync.py     # Синхронизация статистики с Obsidian
mini-app/src/pages/        # Home, GalleryPage, Chalet, Booking
mini-app/src/components/   # NavBar (iOS-стиль)
mini-app/src/config/       # photos.ts (Cloudinary URLs)
.github/workflows/         # deploy-mini-app.yml
Procfile                   # web: python main.py
TZ_v3.0.md                 # Полное техническое задание
PROGRESS.md                # Чеклист задач
_claude/                   # Заметки сессий Claude Code
```

## Правила работы

### Код
- Все commit-сообщения на английском, по конвенции: `feat:`, `fix:`, `docs:`, `chore:`
- После изменений в mini-app — пушить, GitHub Actions задеплоит сам
- После изменений в Python-коде — Railway передеплоится автоматически при пуше
- Не коммитить `.env` — он в `.gitignore`

### Мини-апп (мобильный, iOS)
- `font-size: 16px` на всех `input` и `textarea` — iOS не зумит
- `maximum-scale=1` в viewport — запрет ручного зума
- `type="date"` напрямую, без JS-трюков с onFocus
- `safe-area-inset-bottom` в paddingBottom страниц и NavBar
- Cloudinary URL с `q_auto,f_auto,w_800` для оптимизации

### Railway
- Реальный домен: `worker-production-8fd9.up.railway.app` (не shale-relax-production!)
- Procfile: `web: python main.py` (не worker — иначе нет публичного порта)
- CORS разрешён для `dzbbot-spec.github.io` и `shale-relax.netlify.app`

### GitHub Pages
- Репо должен быть **публичным** (иначе Pages через Actions не работает)
- Vite base: `/shale-relax/` — задаётся через `GITHUB_ACTIONS=true` env
- Workflow запускается только при изменениях в `mini-app/**`

### Память сессий
- Заметки о каждой сессии писать в `_claude/YYYY-MM-DD.md`
- Запускать `utils/obsidian_sync.py` для обновления Obsidian-дашборда
- Полное ТЗ: `TZ_v3.0.md`, прогресс: `PROGRESS.md`

## Решённые проблемы (не наступать снова)

| Проблема | Причина | Решение |
|----------|---------|---------|
| Railway 404 | `Procfile` имел `worker:` | Заменить на `web:` |
| GitHub Pages 404 | Репо был приватным | Сделать публичным |
| Билд падает на CI | Неиспользуемая переменная TypeScript | Убрать `const today` |
| iOS зумит при вводе | `font-size < 16px` | Установить 16px везде |
| Поля дат обрезаются | grid без `min-width:0` | Убрать grid, поля вертикально |
| Неверный Railway URL | Разные домены в коде и реальности | worker-production-8fd9 |
