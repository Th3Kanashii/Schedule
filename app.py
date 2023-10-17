import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import load_config
from bot.handlers import routers_list
from bot.services import on_startup, parse_schedule


async def main() -> None:
    """
    Start the bot.
    """
    config = load_config(path=".env")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        parse_schedule,
        args=["https://asu.pnu.edu.ua/static/groups/1002/014734/"],
        trigger="cron",
        day_of_week="fri",
        hour=15,
        minute=0
    )
    scheduler.start()

    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_routers(*routers_list)

    await asyncio.gather(
        dp.start_polling(bot),
        on_startup(bot)
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
