from aiogram import Router, F
from aiogram.types import Message
from utils.openai_service import get_ai_prediction
from keyboards.help_keyboard import keyboard

router = Router()


TERMS = {
    "rsi": "RSI",
    "ema": "EMA",
    "marketcap": "Рыночная капитализация",
    "price": "Цена",
    "volume": "Объем торгов",
    "signal": "Торговый сигнал",
    "token": "Токен",
    "cryptocurrency": "Криптовалюта",
}


@router.message(F.text.startswith("/help"))
async def cmd_help(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        available = ', '.join(sorted(TERMS.keys()))
        await message.answer(
            f"Для получения объяснения отправьте команду в виде:\n"
            f"`/help rsi`\n\n"
            f"Доступные термины: {available}",
            parse_mode="Markdown", reply_markup=keyboard,
        )
        return

    term = ' '.join(parts[1:]).lower().strip()
    if term not in TERMS:
        available = ', '.join(sorted(TERMS.keys()))
        await message.answer(
            f"Неизвестный термин: {term}\n"
            f"Доступные термины: {available}",
            parse_mode="Markdown", reply_markup=keyboard,
        )
        return

    prompt = (
        f"Объясни термин '{TERMS[term]}' простыми словами для новичка в инвестициях и трейдинге.\n"
        f"Дай определение и короткий пример использования этого термина на практике.\n"
        f"Не используй сложные термины в ответе. Оформи ответ списком, если это удобно."
    )

    # await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    ai_answer = await get_ai_prediction(prompt, max_tokens=300)

    await message.answer(
        f"*Объяснение термина: {TERMS[term]}*\n\n{ai_answer}",
        parse_mode="Markdown"
    )