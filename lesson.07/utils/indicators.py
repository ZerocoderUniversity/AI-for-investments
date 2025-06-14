import pandas as pd
from pandas import DataFrame
from utils.coingecko_service import get_historical_data


def calculate_rsi(prices, period=14):
    """Рассчитываем RSI."""
    prices = pd.Series(prices)

    delta = prices.diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_ema(prices, period=14):
    """Рассчитываем EMA."""
    prices = pd.Series(prices)

    ema = prices.ewm(span=period, adjust=False).mean()

    return ema


def get_rsi(df: DataFrame, period=14):
    """Получить RSI."""
    rsi_series = calculate_rsi(df.price, period=period)

    current_rsi = rsi_series.iloc[-1]

    return current_rsi


def get_ema(df: DataFrame, period=14):
    """Получить EMA."""
    ema_series = calculate_ema(df.price, period=period)

    current_ema = ema_series.iloc[-1]

    return current_ema


def get_simple_signal(rsi_values):
    if rsi_values > 70:
        return "SELL"
    elif rsi_values < 30:
        return "BUY"
    else:
        return "HOLD"


def get_text_signal(signal, coin_id):
    if signal not in ["SELL", "BUY", "HOLD"]:
        text = "Нет такого сигнала"
    elif signal == "SELL":
        text = f"🟥📉 Рекомендация - *продавать* {coin_id}"
    elif signal == "BUY":
        text = f"🟩📈 Рекомендация - *покупать* {coin_id}"
    elif signal == "HOLD":
        text = f"🟨⏸️ Рекомендация - *держать* {coin_id}"

    return text



if __name__ == '__main__':



    df = get_historical_data('bitcoin', days=30)
    # rsi_series = calculate_rsi(df.price, period=14)
    # ema_series = calculate_ema(df.price, period=14)
    #
    # current_rsi = rsi_series.iloc[-1]
    # current_ema = ema_series.iloc[-1]

    current_rsi = get_rsi(df)
    current_ema = get_ema(df)

    print(f"Текущий RSI {current_rsi}")
    print(f"Текущий EMA {current_ema}")
