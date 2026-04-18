"""Планировщик: автозапуск ИИ-конвейера по расписанию (пн-вс, 10:00-12:00 МСК)."""

from __future__ import annotations

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from config import get_settings
from pipeline.pipeline import run_pipeline
from utils.logger import setup_logger

_settings = get_settings()
_logger = setup_logger("scheduler", _settings.log_level, _settings.logs_path)


async def pipeline_job() -> None:
    """Задача планировщика: один запуск конвейера."""
    _logger.info("Планировщик: запуск конвейера по расписанию.")
    try:
        await run_pipeline()
    except Exception as exc:  # noqa: BLE001
        _logger.error("Конвейер завершился с ошибкой: %s", exc)


async def main() -> None:
    """Запускает планировщик и держит его активным."""
    tz = timezone(_settings.timezone)
    scheduler = AsyncIOScheduler(timezone=tz)

    # Запуск в 10:00, 11:00 и 12:00 по МСК каждый день недели
    trigger = CronTrigger(day_of_week="mon-sun", hour="10,11,12", minute=0, timezone=tz)
    scheduler.add_job(
        pipeline_job,
        trigger=trigger,
        id="daily_content_pipeline",
        replace_existing=True,
    )

    scheduler.start()
    _logger.info(
        "Планировщик активен. Окно публикаций: пн-вс 10:00, 11:00, 12:00 (%s).",
        _settings.timezone,
    )

    try:
        # Бесконечный цикл — планировщик работает пока процесс жив
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        _logger.info("Планировщик остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
