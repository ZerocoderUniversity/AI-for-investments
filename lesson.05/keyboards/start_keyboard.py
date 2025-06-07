from aiogram import types


button_start = types.KeyboardButton(text="/start")
button_help = types.KeyboardButton(text="/help")
button_info = types.KeyboardButton(text="/info")
button_analyze_bitcoin = types.KeyboardButton(text="/analyze")
button_analyze_ethereum = types.KeyboardButton(text="/price")

kb = [
    [button_start, button_help, button_info],
    [button_analyze_bitcoin, button_analyze_ethereum],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
