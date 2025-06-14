from aiogram import types


button_chart_bitcoin = types.KeyboardButton(text="/chart bitcoin")
button_chart_ethereum = types.KeyboardButton(text="/chart ethereum")

kb = [
    [button_chart_bitcoin, button_chart_ethereum],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)



button_chart_ai_bitcoin = types.KeyboardButton(text="/chart_ai bitcoin")
button_chart_ai_ethereum = types.KeyboardButton(text="/chart_ai ethereum")

kb_ai = [
    [button_chart_ai_bitcoin, button_chart_ai_ethereum],
]

keyboard_ai = types.ReplyKeyboardMarkup(keyboard=kb_ai, resize_keyboard=True)


button_timing_bitcoin = types.KeyboardButton(text="/timing bitcoin")
button_timing_ethereum = types.KeyboardButton(text="/timing ethereum")

kb_timing = [
    [button_timing_bitcoin, button_timing_ethereum],
]

keyboard_timing = types.ReplyKeyboardMarkup(keyboard=kb_timing, resize_keyboard=True)