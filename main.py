import os
import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher

from database.engine import session_maker, create_db, drop_db
from handlers import main_handler
from middlewares.db import DataBaseSession


load_dotenv(find_dotenv())
TOKEN=os.getenv('BOT_TOKEN')


async def main():
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)

    bot=Bot(token=TOKEN, default=default)
    dp=Dispatcher()

    dp.startup.register(create_db)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    dp.include_router(main_handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот спит')