from multiprocessing.connection import answer_challenge

from aiogram import Router, F, Bot
# from aiogram.client import bot
from aiogram.types import Message, FSInputFile
from utils.plot_service import plot_price_chart, explain_chart
import os
from pathlib import Path
from keyboards import chart_keyboard


router = Router()

@router.message(F.text.startswith("/chart"))
async def chart_crypto(message: Message, bot: Bot):
    """Обработчик команды /chart coin_id"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer('Введите команду в виде: /chart bitcoin', reply_markup=chart_keyboard.keyboard)
        return

    coin_id = parts[1].lower().strip()

    await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")

    chart_path = plot_price_chart(coin_id)

    chart_file = Path(chart_path) if chart_path else None

    if chart_file and chart_file.exists():
        # with open(chart_file, "rb") as photo:
        photo = FSInputFile(chart_file)
        await message.answer_photo(photo, caption=f"График {coin_id}", parse_mode="Markdown")
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        answer_explain_chart = await explain_chart(coin_id)
        await message.answer(f"Коментарий к графику по {coin_id}\n\n{answer_explain_chart}", parse_mode="Markdown")

    else:
        await message.answer(f"Не удалось построить график по {coin_id}. Возможно, нет данных или ошибка названия.")
