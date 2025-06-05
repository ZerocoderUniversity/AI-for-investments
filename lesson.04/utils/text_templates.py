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
