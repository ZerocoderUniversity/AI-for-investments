import asyncio
from aiogram import Bot, Dispatcher
import config
import logging
from handlers import common, crypto_analyze, ai_help


async def main():
    """"""

    # Подключаем логгирование
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.TOKEN_TG)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(crypto_analyze.router)
    dp.include_router(ai_help.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())