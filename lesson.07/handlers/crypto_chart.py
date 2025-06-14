from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from utils.plot_service import plot_price_chart, explain_chart, plot_crypto_chart_with_indicators
from utils.openai_service import get_ai_prediction
from utils.coingecko_service import get_historical_data
from utils.indicators import calculate_rsi, calculate_ema
from utils.news_service import get_latest_news
from datetime import datetime
import pandas as pd
from pathlib import Path
from keyboards import chart_keyboard


router = Router()


@router.message(F.text.startswith("/chart_ai"))
async def chart_ai_crypto(message: Message, bot: Bot):
    """Обработчик команды /chart_ai coin_id"""

    parts = message.text.strip().split()
    print(parts)
    if len(parts) < 2:
        await message.answer('Введите команду в виде: /chart_ai bitcoin', reply_markup=chart_keyboard.keyboard_ai)
        return

    coin_id = parts[1].lower().strip()

    await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")

    df = get_historical_data(coin_id, days=60)
    if df.empty or df is None:
        await message.answer(f'Не удалось получить данные для {coin_id}')
        return

    chart_path = plot_crypto_chart_with_indicators(df, coin_id)

    chart_file = Path(chart_path) if chart_path else None

    if chart_file and chart_file.exists():
        # with open(chart_file, "rb") as photo:
        photo = FSInputFile(chart_file)
        await message.answer_photo(photo, caption=f"График {coin_id}", parse_mode="Markdown")
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        golden_cross = df['signal'].eq(1).any()
        death_cross = df['signal'].eq(-1).any()

        if golden_cross or death_cross:
            pattern_text = ""
            if golden_cross:
                pattern_text += "На графике обнаружен паттерн 'золотой крест' (EMA14 пересекает EMA50 снизу вверх).\n"
            if death_cross:
                pattern_text += "Также обнаружен паттерн 'мёртвый крест' (EMA14 пересекает EMA50 сверху вниз).\n"

            prompt = (
                f"{pattern_text}\n"
                "Объясни, что это значит для трейдера и какие возможные последствия. "
                "Дай краткий совет по действию (входить, держать или выходить)."
            )

            await message.answer("🤖 Обрабатываю паттерн... Жду пояснения от AI.")
            ai_response = await get_ai_prediction(prompt)
            await message.answer(
                f"🧠 <b>AI-комментарий по паттерну:</b>\n{ai_response}",
                parse_mode="HTML"
            )


        # answer_explain_chart = await explain_chart(coin_id)
        # await message.answer(f"Коментарий к графику по {coin_id}\n\n{answer_explain_chart}", parse_mode="Markdown")

    else:
        await message.answer(f"Не удалось построить график по {coin_id}. Возможно, нет данных или ошибка названия.")



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


@router.message(F.text.startswith("/timing"))
async def timing_crypto(message: Message, bot: Bot):
    """Обработчик команды /timing coin_id"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer('Введите команду в виде: /timing bitcoin', reply_markup=chart_keyboard.keyboard_timing)
        return

    coin_id = parts[1].lower().strip()

    df = get_historical_data(coin_id, days=60)
    if df.empty or df is None:
        await message.answer(f'Не удалось получить данные для {coin_id}')
        return

    df['RSI'] = calculate_rsi(df['price'], 14)
    df['EMA14'] = calculate_ema(df['price'], 14)
    df['EMA50'] = calculate_ema(df['price'], 50)

    last_rsi = df['RSI'].iloc[-1]
    last_ema14 = df['EMA14'].iloc[-1]
    last_ema50 = df['EMA50'].iloc[-1]

    last_date = df.index[-1] if isinstance(df.index, pd.DatetimeIndex) else df['date'].iloc[-1]
    if isinstance(last_date, pd.Timestamp):
        weekday = last_date.strftime('%A')
        date_str = last_date.strftime('%Y-%m-%d')
    else:
        weekday = str(last_date)
        date_str = str(last_date)

    news_titles = get_latest_news(coin_id, 5)
    news_text = '\n'.join([f'— {title}' for title in news_titles]) if news_titles else 'нет данных по новостям'


    prompt = (
        f"Сегодня {weekday} ({date_str}). "
        f"Текущие индикаторы по монете {coin_id.upper()}:\n"
        f"- RSI(14): {last_rsi:.2f}\n"
        f"- EMA(14): {last_ema14:.2f}\n"
        f"- EMA(50): {last_ema50:.2f}\n"
        f"- Свежие новости: {news_text}\n"
        "\n"
        "Проанализируй, есть ли сигналы перекупленности или перепроданности, пересечения EMA, и какие риски связаны с текущим моментом недели. "
        "Стоит ли открывать сделку сейчас или подождать? Ответь простыми словами для новичка, объясни на что обратить внимание. "
        "Если можешь — дай короткий совет (входить, держать, ждать, избегать сделок)."
    )

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    ai_answer = await get_ai_prediction(prompt, max_tokens=400)

    await message.answer(
        f"🧠 <b>AI-комментарий по таймингу входа:</b>\n{ai_answer}",
        parse_mode="HTML"
    )