from pycoingecko import CoinGeckoAPI
from datetime import datetime, timezone
import pandas as pd
from pprint import pprint


pd.set_option('display.float_format', '{:,.2f}'.format)
cg = CoinGeckoAPI()


def get_current_price(coin_id: str, currency: str = "usd"):
    """Получить текущую цену монеты с CoinGecko."""

    try:
        data = cg.get_price(ids=coin_id, vs_currencies=currency)
    except Exception as e:
        print(f"Ошибка при запросе данных к CoinGecko - {e}")
        return None

    if coin_id in data and currency in data.get(coin_id):
        return data.get(coin_id).get(currency)
    else:
        return None


def get_historical_data(coin_id: str, currency: str = "usd", days: int = 60):
    """Получить исторические данные по монете."""

    try:
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=currency, days=days)
    except Exception as e:
        print(f"Ошибка при запросе данных к CoinGecko - {e}")
        return None

    if "prices" not in data or "total_volumes" not in data:
        print("Нет нужных данных")
        return None

    prices = data.get("prices")
    volumes = data.get("total_volumes")

    date_list = []
    price_list = []
    volume_list = []


    for price, volume in zip(prices, volumes):
        timestamp = price[0] / 1000
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        date_list.append(dt)
        price_list.append(price[1])
        volume_list.append(volume[1])

    df = pd.DataFrame({"date": date_list, "price": price_list, "volume": volume_list})

    return df


def get_daily_summary(coin_id: str, currency: str = "usd"):
    """Функция для краткого отчета за сутки"""

    try:
        df = get_historical_data(coin_id=coin_id, currency=currency, days=1)
    except Exception as e:
        print(f"Ошибка при запросе данных к CoinGecko - {e}")
        return None

    if df is None or len(df) == 0:
        return None

    current_price = df["price"].iloc[-1]
    min_price = df["price"].min()
    max_price = df["price"].max()
    total_volume = df["volume"].sum()


    summary = {
        "current_price": current_price,
        "min_price": min_price,
        "max_price": max_price,
        "total_volume": total_volume,
    }

    return summary


if __name__ == '__main__':
    # price = get_current_price(coin_id="ethereum", currency="rub")
    # print(price)

    data = get_historical_data(coin_id="bitcoin", currency="rub", days=90)
    # print(data.head(20))
    print(data.tail(20))