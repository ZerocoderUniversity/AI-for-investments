from aiogram import types


button_start = types.KeyboardButton(text="/start")
button_help = types.KeyboardButton(text="/help")
button_info = types.KeyboardButton(text="/info")
button_analyze = types.KeyboardButton(text="/analyze")
button_price = types.KeyboardButton(text="/price")
button_chart = types.KeyboardButton(text="/chart")

kb = [
    [button_start, button_help, button_info],
    [button_analyze, button_price, button_chart],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
