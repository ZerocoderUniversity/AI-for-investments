from aiogram import Router, F, Bot
from aiogram.types import Message
from utils.coingecko_service import get_current_price, get_daily_summary, get_historical_data
from utils.indicators import get_ema, get_rsi, get_simple_signal, get_text_signal
from utils.text_templates import format_signal_message, get_signal_interpretation, make_ai_prompt
from utils.openai_service import get_ai_prediction
from keyboards import analyze_keyboar, price_keyboard


router = Router()


@router.message(F.text.startswith("/analyze"))
async def analyze_crypto(message: Message, bot: Bot):
    """Обработчик команды /analyze coin_id"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer('Введите команду в виде: /analyze bitcoin', reply_markup=analyze_keyboar.keyboard)
        return

    coin_id = parts[1].lower().strip()

    summary = get_daily_summary(coin_id)
    if summary is None:
        await message.answer(f'Монета с id {coin_id} не найдена')
        return

    df = get_historical_data(coin_id, days=30)
    current_rsi = get_rsi(df)
    current_ema = get_ema(df)

    signal_rsi = get_simple_signal(current_rsi)
    signal_rsi_text = get_text_signal(signal_rsi, coin_id)
    signal_interpretation = get_signal_interpretation(signal_rsi)


    # Изменения за сутки и за неделю-месяц
    price_change_24h = df['price'].iloc[-1] - df['price'].iloc[-2]
    percent_change_24h = price_change_24h / df['price'].iloc[-2] * 100

    price_change_30d = df['price'].iloc[-1] - df['price'].iloc[0]
    percent_change_30d = price_change_30d / df['price'].iloc[0] * 100

    current_market_cap = df['market_caps'].iloc[-1] if "market_caps" in df.columns else None

    current_market_cap_rank = None

    prompt = make_ai_prompt(
        coin_id,
        summary,
        current_rsi,
        current_ema,
        price_change_24h,
        percent_change_24h,
        price_change_30d,
        percent_change_30d,
        current_market_cap,
    )

    text = format_signal_message(coin_id, summary, current_rsi, current_ema, signal_rsi_text, signal_interpretation)
    # print(text)
    await message.answer(text, parse_mode="Markdown")

    # print(prompt)
    # await message.answer_chat_action("typing")
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    ai_answer = await get_ai_prediction(prompt)

    # print("*" * 30)
    # print(ai_answer)
    await message.answer(
        f"*AI-прогноз по {coin_id}*:\n\n{ai_answer}",
        parse_mode="Markdown"
    )


@router.message(F.text.startswith("/price"))
async def price_crypto(message: Message):
    """Обработчик команды /price coin_id"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer('Введите команду в виде: /price bitcoin', reply_markup=price_keyboard.keyboard)
        return

    coin_id = parts[1].lower().strip()

    price = get_current_price(coin_id)

    if price is None:
        await message.answer(f'Монета с id {coin_id} не найдена')
        return

    text = f'Текущая цена {coin_id}: {price} usd'

    await message.answer(text, parse_mode="Markdown")


if __name__ == '__main__':
    pass
