# PROGRESS.md — Шале Релакс Automation

## Статус проекта: 🟢 Бот работает

Последнее обновление: **18 апреля 2026**

---

## ✅ Готово

### Инфраструктура
- [x] Структура проекта (`bot/`, `pipeline/`, `utils/`, `prompts/`)
- [x] `.env` заполнен ключами (Telegram, OpenAI, Kling)
- [x] `requirements.txt` — aiogram 3.x + httpx + pydantic-settings
- [x] Виртуальное окружение `.venv`, зависимости установлены
- [x] `.gitignore` — `.env` и медиафайлы защищены

### Telegram-бот
- [x] FSM-сценарий бронирования: имя → даты → гости → контакт
- [x] Заявка пересылается владельцу в Telegram (OWNER_CHAT_ID=1914219730)
- [x] Заявка сохраняется в `data/bookings.json`
- [x] FAQ: как добраться, что посмотреть, эндуро, трансфер
- [x] Приём фото от управляющего → сохранение в `data/photos/`
- [x] Файловый FSM-storage (`data/fsm_storage.json`) — состояние не теряется при рестарте
- [x] **Протестировано end-to-end: заявка дошла до владельца**

### ИИ-конвейер (код написан, не протестирован с реальными ключами)
- [x] `kling.py` — генерация видео через Kling AI (JWT-аутентификация)
- [x] `gpt.py` — подписи через OpenAI + фильтр запрещённых слов
- [x] `smmbox.py` — скачивание видео в `ready_to_post/` + уведомление владельцу
- [x] `pipeline.py` — оркестратор конвейера
- [x] `scheduler.py` — APScheduler, пн-вс 10:00-12:00 МСК
- [x] `prompts/kling_prompts.json` — 12 промптов по рубрикам

---

## 🔜 Следующие шаги

### Шаг 1 — Тест конвейера (ближайший)
- [ ] Положить 1 фото в `data/photos/`
- [ ] `cd shale-relax && source .venv/bin/activate && python -m pipeline.pipeline`
- [ ] Убедиться: видео появилось в `ready_to_post/`, пришло уведомление в Telegram

### Шаг 2 — Управляющий
- [ ] Управляющий пишет `/start` боту
- [ ] Узнать его chat_id через @userinfobot
- [ ] Добавить в `.env`: `MANAGER_CHAT_ID=...`
- [ ] Отправить тестовое фото → проверить сохранение в `data/photos/`

### Шаг 3 — Smmbox (автопубликация в Instagram)
- [ ] Оплатить тариф на smmbox.com
- [ ] Подключить Instagram @shale_relax_elbrus
- [ ] Добавить в `.env`: `SMMBOX_API_KEY=...`, `SMMBOX_ACCOUNT_ID=...`
- [ ] Обновить `smmbox.py` для публикации через Smmbox API

### Шаг 4 — VPS (работа 24/7)
- [ ] Арендовать VPS (Hetzner/FirstVDS, ~500 руб/мес)
- [ ] Перенести проект, настроить `.env`
- [ ] Запустить бота как systemd-сервис

---

## 📋 Ключи и доступы

| Сервис | Статус |
|---|---|
| Telegram Bot Token | ✅ Активен (новый, после revoke) |
| OpenAI API Key | ✅ Активен |
| Kling Access Key + Secret Key | ✅ Настроены |
| MANAGER_CHAT_ID / MANAGER_USERNAME | ⚠️ Не задан |
| Smmbox | ❌ Нет тарифа |
| VPS | ❌ Не арендован |
