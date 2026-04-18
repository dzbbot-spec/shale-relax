"""Точка входа: бот + планировщик конвейера в одном процессе."""

from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from bot.handlers import router
from config import get_settings
from pipeline.pipeline import run_pipeline
from utils.logger import setup_logger

_bot_instance: Bot | None = None


async def health(request: web.Request) -> web.Response:
    return web.Response(text="ok")


async def booking_webhook(request: web.Request) -> web.Response:
    """Принимает заявки на бронирование из Mini App."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "invalid json"}, status=400)

    settings = get_settings()
    if not settings.owner_chat_id:
        return web.json_response({"error": "owner not configured"}, status=500)

    check_in = data.get("check_in", "—")
    check_out = data.get("check_out", "—")
    dates = f"{check_in} → {check_out}" if check_in != "—" else "—"

    text = (
        "📋 *Заявка из Mini App*\n"
        "─────────────────────────\n"
        f"👤 Имя:     {data.get('name', '—')}\n"
        f"📅 Даты:    {dates}\n"
        f"👥 Гостей:  {data.get('guests', '—')}\n"
        f"📞 Контакт: {data.get('contact', '—')}\n"
        f"💬 Коммент: {data.get('comment', '—')}\n"
        f"🕐 Время:   {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        "─────────────────────────"
    )

    if _bot_instance:
        try:
            await _bot_instance.send_message(
                chat_id=settings.owner_chat_id,
                text=text,
                parse_mode="Markdown",
            )
        except Exception as exc:
            logger = setup_logger("bot", settings.log_level, settings.logs_path)
            logger.error("Ошибка отправки заявки владельцу: %s", exc)

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    return web.json_response({"status": "ok"}, headers=headers)


async def booking_preflight(request: web.Request) -> web.Response:
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    return web.Response(status=204, headers=headers)


async def start_health_server() -> None:
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_post("/api/booking", booking_webhook)
    app.router.add_route("OPTIONS", "/api/booking", booking_preflight)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()


async def main() -> None:
    settings = get_settings()
    logger = setup_logger("bot", settings.log_level, settings.logs_path)

    if not settings.telegram_bot_token:
        logger.critical("TELEGRAM_BOT_TOKEN не задан в .env. Бот не запущен.")
        return

    # ── Health-check сервер для Railway ──────────────────────────────────────
    await start_health_server()

    # ── Планировщик конвейера ─────────────────────────────────────────────
    tz = timezone(settings.timezone)
    scheduler = AsyncIOScheduler(timezone=tz)
    scheduler.add_job(
        run_pipeline,
        CronTrigger(day_of_week="mon-sun", hour="10,11,12", minute=0, timezone=tz),
        id="daily_pipeline",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Планировщик активен: пн-вс 10:00, 11:00, 12:00 МСК")

    # ── Telegram-бот ──────────────────────────────────────────────────────
    global _bot_instance
    bot = Bot(token=settings.telegram_bot_token)
    _bot_instance = bot
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    logger.info("Бот @shale_relax_bot запущен. Ожидание сообщений...")

    try:
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    except Exception as exc:  # noqa: BLE001
        logger.error("Бот остановлен с ошибкой: %s", exc)
    finally:
        scheduler.shutdown()
        await bot.session.close()
        logger.info("Бот остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
