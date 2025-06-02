from aiogram import Router, F
from aiogram.types import Message
from utils.coingecko_service import get_current_price, get_daily_summary


router = Router()


@router.message(F.text.startswith("/analyze"))
async def analyze_crypto(message: Message):
    """Обработчик команды /analyze coin_id"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer('Введите команду в виде: /analyze bitcoin')
        return

    coin_id = parts[1].lower().strip()

    # price = get_current_price(coin_id)
    # if price is None:
    #     await message.answer(f'Монета с id {coin_id} не найдена')
    #     return
    #
    # result = f'Текущая цена {coin_id}: {price} usd'
    # await message.answer(result)

    summary = get_daily_summary(coin_id)
    if summary is None:
        await message.answer(f'Монета с id {coin_id} не найдена')
        return

    text = f""" *{coin_id}* (за 24 часа)
*Цена* {summary["current_price"]:.2f} USD
*Min цена* {summary["min_price"]:.2f} USD
*Max Цена* {summary["max_price"]:.2f} USD
*Объем* {summary["total_volume"]:.2f} USD"""

    await message.answer(text, parse_mode="Markdown")


@router.message(F.text.startswith("/price"))
async def price_crypto(message: Message):
    """Обработчик команды /price coin_id"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer('Введите команду в виде: /price bitcoin')
        return

    coin_id = parts[1].lower().strip()

    price = get_current_price(coin_id)

    if price is None:
        await message.answer(f'Монета с id {coin_id} не найдена')
        return

    text = f'Текущая цена {coin_id}: {price} usd'

    await message.answer(text, parse_mode="Markdown")