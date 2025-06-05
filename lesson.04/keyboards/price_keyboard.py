from aiogram import types


button_price_bitcoin = types.KeyboardButton(text="/price bitcoin")
button_price_ethereum = types.KeyboardButton(text="/price ethereum")

kb = [
    [button_price_bitcoin, button_price_ethereum],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)