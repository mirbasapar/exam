import asyncio
from aiogram import Bot
import logging
from handlers.echo import echo_router
from handlers.survey import survey_router
from config import bot, dp, database


async def on_startup(bot: Bot):
    await database.create_tables()


async def main():
    dp.include_router(survey_router)
    dp.include_router(echo_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
