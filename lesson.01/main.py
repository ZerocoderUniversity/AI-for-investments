import asyncio
from aiogram import Bot, Dispatcher
import config
from handlers import common


async def main():
    bot = Bot(token=config.TOKEN_TG)
    dp = Dispatcher()

    dp.include_router(common.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())