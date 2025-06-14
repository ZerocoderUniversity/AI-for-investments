from aiogram import types


button_help_rsi = types.KeyboardButton(text="/help rsi")
button_help_ema = types.KeyboardButton(text="/help ema")
button_help_price = types.KeyboardButton(text="/help price")
button_help_volume = types.KeyboardButton(text="/help volume")
button_help_marketcap = types.KeyboardButton(text="/help marketcap")
button_help_signal = types.KeyboardButton(text="/help signal")
button_help_token = types.KeyboardButton(text="/help token")

kb = [
    [button_help_rsi, button_help_ema, button_help_price, button_help_volume],
    [button_help_marketcap, button_help_signal, button_help_token],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
