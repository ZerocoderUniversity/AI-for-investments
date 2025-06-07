def format_signal_message(coin_id, summary, current_rsi, current_ema, signal_rsi_text, signal_interpretation) -> str:
    text = f""" *{coin_id}* (за 24 часа)
    *Цена* {summary["current_price"]:.2f} USD
    *💵Min цена* {summary["min_price"]:.2f} USD
    *💵Max Цена* {summary["max_price"]:.2f} USD
    *Объем* {summary["total_volume"]:.2f} USD
    *💵RSI* {current_rsi:.2f} USD
    *EMA* {current_ema:.2f} USD
    {signal_rsi_text}
    {signal_interpretation}"""

    return text


def get_signal_interpretation(signal):
    if signal == "BUY":
        return """Сигнал BUY: RSI ниже 30 - актив перепродан.
        Это может говорить о том, что цена достигла минимума, и ожидается рост"""
    elif signal == "SELL":
        return """Сигнал SELL: RSI выше 70 - актив перекуплен.
        Это значит, что цена слишком быстро росла и возможен разворот вниз"""
    else:
        return """Сигнал HOLD: RSI находится в диапазоне от 30 до 70.
        Это зона неопределенности"""


def make_ai_prompt(
    coin_id,
    summary,
    current_rsi,
    current_ema,
    price_change_24h,
    percent_change_24h,
    price_change_30d,
    percent_change_30d,
    current_market_cap=None,
    current_market_cap_rank=None
):
    """Собирает информативный промпт для ИИ"""
    prompt = f"""
Дай кhаткий инвестиционный прогноз по монете {coin_id} на основе следующих данных:
- Текущая цена: {summary['current_price']:.2f} USD
- Минимальная цена за сутки: {summary['min_price']:.2f} USD
- Объём торгов за сутки: {summary['total_volume']:.2f} USD
- RSI: {current_rsi:.2f}
- EMA: {current_ema:.2f}
- Изменение цены за сутки: {price_change_24h:+.2f} USD ({percent_change_24h:+.2f}%)
- Изменение цены за неделю: {price_change_30d:+.2f} USD ({percent_change_30d:+.2f}%)\n
"""

    if current_market_cap is not None:
        prompt += f"- Рыночная капитализация: {current_market_cap:,.0f} USD\n"
    if current_market_cap_rank is not None:
        prompt += f"- Место в рейтинге: {current_market_cap_rank}\n"

    prompt += (
        "\nСделай вывод и аргументируй решение (почему именно такой совет), объясни простым языком для новичка, какие факторы сейчас наиболее важны."
    )
    return prompt