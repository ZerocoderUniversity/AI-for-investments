from aiogram import Router, types
from aiogram.filters import Command
from keyboards.start_keyboard import keyboard


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я ИИ-ассистент инвестор. Напиши /help, чтобы узнать, что я умею",
                         reply_markup=keyboard)


@router.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer("""Я умею:
    - Получать дневной отчет по криптовалюте */analyze bitcoin*.
    - Анализировать рынок
    - Строить графики
    - Работать с файлами""")