import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from handlers import main_handler

load_dotenv(find_dotenv())
TOKEN=os.getenv('TOKEN')
async def main():

    bot=Bot(token=TOKEN)
    dp=Dispatcher()
    dp.include_router(main_handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот спит')