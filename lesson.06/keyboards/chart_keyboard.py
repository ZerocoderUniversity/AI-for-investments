from aiogram import types


button_chart_bitcoin = types.KeyboardButton(text="/chart bitcoin")
button_chart_ethereum = types.KeyboardButton(text="/chart ethereum")

kb = [
    [button_chart_bitcoin, button_chart_ethereum],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)