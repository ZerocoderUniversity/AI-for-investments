from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from utils.coingecko_service import get_historical_data
from utils.indicators import calculate_rsi, calculate_ema, get_simple_signal
from utils.openai_service import get_ai_prediction


def plot_price_chart(coin_id, days=30):

    df = get_historical_data(coin_id, days=days)

    if df is None or df.empty:
        return None

    charts_dir = Path("charts")

    if not charts_dir.exists():
        charts_dir.mkdir(parents=True)

    ema = calculate_ema(df["price"], period=14)

    rsi = calculate_rsi(df["price"], period=14)

    fig, (ax_price, ax_rsi) = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    fig.suptitle(f"{coin_id.capitalize()} — Цена, EMA и RSI", fontsize=15)

    ax_price.plot(df["date"], df["price"], label="Цена", linewidth=2)

    ax_price.plot(df["date"], ema, label="EMA (14)", linestyle="--")

    ax_price.set_ylabel("Цена (USD)")
    ax_price.legend(loc="upper left")
    ax_price.grid(True, alpha=0.3)

    signals = [get_simple_signal(r) for r in rsi]

    colors = {"BUY": "green", "SELL": "red", "HOLD": "yellow"}

    last_signal = None
    start_idx = 0

    for idx, sig in enumerate(signals):
        if sig != last_signal and last_signal is not None:
            ax_price.axvspan(
                df["date"].iloc[start_idx], df["date"].iloc[idx - 1],
                color=colors.get(last_signal, "grey"), alpha=0.07
            )
            start_idx = idx
        last_signal = sig
    ax_price.axvspan(
        df["date"].iloc[start_idx], df["date"].iloc[-1],
        color=colors.get(last_signal, "grey"), alpha=0.07
    )

    ax_rsi.plot(df["date"], rsi, label="RSI (14)", color="purple")

    ax_rsi.axhline(70, color="red", linestyle="--", alpha=0.7, label="RSI 70 (SELL)")
    ax_rsi.axhline(30, color="green", linestyle="--", alpha=0.7, label="RSI 30 (BUY)")
    ax_rsi.set_ylabel("RSI")
    ax_rsi.set_xlabel("Дата")
    ax_rsi.legend(loc="upper left")
    ax_rsi.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fname = charts_dir / f"{coin_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(fname)
    plt.close(fig)

    return str(fname)


def explain_chart(coin_id, days=30):
    df = get_historical_data(coin_id, days=days)

    if df is None or df.empty:
        return None

    ema = calculate_ema(df["price"], period=14)

    rsi = calculate_rsi(df["price"], period=14)

    last_price = df["price"].iloc[-1]
    last_ema = ema.iloc[-1]
    last_rsi = rsi.iloc[-1]
    date_str = df["date"].iloc[-1].strftime('%Y-%m-%d')


    prompt = (
        f"Проанализируй график по монете {coin_id} за последние 30 дней.\n"
        f"Вот ключевые данные на {date_str}:\n"
        f"- Текущая цена: {last_price:.2f} USD\n"
        f"- EMA(14): {last_ema:.2f}\n"
        f"- RSI(14): {last_rsi:.2f}\n"
        f"\n"
        f"Изменения цены:\n"
        f"{', '.join(f'{p:.2f}' for p in df['price'].tail(7))}\n"
        f"\n"
        f"Значения EMA за 7 дней:\n"
        f"{', '.join(f'{e:.2f}' for e in ema.tail(7))}\n"
        f"\n"
        f"Значения RSI за 7 дней:\n"
        f"{', '.join(f'{r:.2f}' for r in rsi.tail(7))}\n"
        f"\n"
        f"Дай короткий комментарий к ситуации: что видно по динамике цены, EMA и RSI? Есть ли сигналы для трейдера?\n"
        f"Поясни для новичка!"
    )

    ai_answer = get_ai_prediction(prompt, max_tokens=400)

    return ai_answer


def plot_crypto_chart_with_indicators(df: pd.DataFrame, coin_id: str) -> str:
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['EMA14'] = calculate_ema(df['price'], 14)
    df['EMA50'] = calculate_ema(df['price'], 50)
    df['RSI'] = calculate_rsi(df['price'], 14)

    df['signal'] = 0
    df.loc[
        (df['EMA14'] > df['EMA50']) & (df['EMA14'].shift(1) <= df['EMA50'].shift(1)),
        'signal'
    ] = 1

    df.loc[
        (df['EMA14'] < df['EMA50']) & (df['EMA14'].shift(1) >= df['EMA50'].shift(1)),
        'signal'
    ] = -1



    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(12, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]}
    )

    ax1.plot(df.index, df['price'], label='Price', color='black')
    ax1.plot(df.index, df['EMA14'], label='EMA14', linestyle='--', color='blue')
    ax1.plot(df.index, df['EMA50'], label='EMA50', linestyle='--', color='orange')

    for idx, row in df.iterrows():
        if row['signal'] == 1:
            ax1.scatter(idx, row['price'], color='green', marker='^', s=100)
        elif row['signal'] == -1:
            ax1.scatter(idx, row['price'], color='red', marker='v', s=100)

    ax1.scatter([], [], color='green', marker='^', s=100, label='Golden Cross')
    ax1.scatter([], [], color='red', marker='v', s=100, label='Death Cross')

    ax1.set_title(f'{coin_id.upper()} Price with EMA14/50')
    ax1.set_ylabel('Price')
    ax1.legend(loc='upper left')

    ax2.plot(df.index, df['RSI'], label='RSI', color='purple')
    ax2.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    ax2.axhline(30, color='green', linestyle='--', label='Oversold (30)')

    ax2.fill_between(df.index, 70, 100, color='red', alpha=0.1)
    ax2.fill_between(df.index, 0, 30, color='green', alpha=0.1)

    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)

    ax2.set_title('RSI (14)')
    ax2.legend(loc='upper left')

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))


    plt.tight_layout()
    charts_dir = Path("charts")
    charts_dir.mkdir(exist_ok=True)

    filename = f"{coin_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = charts_dir / filename

    plt.savefig(filepath)
    plt.close()
    return str(filepath)
