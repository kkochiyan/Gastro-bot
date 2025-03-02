from aiogram import Bot, Dispatcher

from handlers import routes
from bot import BOT_TOKEN
from database import async_main

import asyncio

async def main():
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    for router in routes:
        dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')