import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from keyboards.menu import set_commands
from handlers.handlers import router

async def main():
    load_dotenv()
    bot=Bot(token=os.getenv('BOT_TOKEN'))
    dp=Dispatcher()
    dp.include_router(router)
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')