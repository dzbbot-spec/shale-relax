"""Точка входа: бот + планировщик конвейера в одном процессе."""

from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from bot.handlers import router
from config import get_settings
from pipeline.pipeline import run_pipeline
from utils.logger import setup_logger


async def main() -> None:
    settings = get_settings()
    logger = setup_logger("bot", settings.log_level, settings.logs_path)

    if not settings.telegram_bot_token:
        logger.critical("TELEGRAM_BOT_TOKEN не задан в .env. Бот не запущен.")
        return

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
    bot = Bot(token=settings.telegram_bot_token)
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
