import requests
from config import CRYPTOPANIC, BASE_URL_NEWS


def get_latest_news(coin_id: str, limit: int = 3):
    url = f"{BASE_URL_NEWS}?auth_token={CRYPTOPANIC}&currencies={coin_id}&public=true"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return [item['title'] for item in data['results'][:limit]]
    except Exception:
        return []


if __name__ == '__main__':
    crypto_list = get_latest_news('BTC')
    print(crypto_list)