from aiogram import types


button_analyze_bitcoin = types.KeyboardButton(text="/analyze bitcoin")
button_analyze_ethereum = types.KeyboardButton(text="/analyze ethereum")

kb = [
    [button_analyze_bitcoin, button_analyze_ethereum],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)