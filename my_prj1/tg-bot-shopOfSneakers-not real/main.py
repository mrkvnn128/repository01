import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv

from handlers.handlers import router
from database.models import async_main

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
async def main():
    await async_main()
    if not BOT_TOKEN:
        raise ValueError("Токен бота не найден. Проверьте .env файл!")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Отключение бота')

