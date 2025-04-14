import requests
import time
import statistics

BOT_TOKEN = "7744317479:AAGWhMOivMNuDwU5iCp4pAYf3lx50YFU-Aw"
CHANNEL_USERNAME = "@samir80s"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_USERNAME,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def get_klines(symbol, interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        closes = [float(entry[4]) for entry in data]
        return closes
    except Exception as e:
        print(f"[WARNING] Could not fetch klines for {symbol}: {e}")
        return None

def calculate_ema(prices, period):
    emas = []
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices:
        ema = price * k + ema * (1 - k)
        emas.append(ema)
    return emas

def calculate_rsi(prices, period=14):
    gains, losses = [], []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))
    avg_gain = statistics.mean(gains[-period:])
    avg_loss = statistics.mean(losses[-period:])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def generate_signal(symbol, closes):
    if len(closes) < 50:
        return None

    ema20 = calculate_ema(closes, 20)[-1]
    ema50 = calculate_ema(closes, 50)[-1]
    rsi = calculate_rsi(closes, 14)
    current_price = closes[-1]

    if current_price > ema20 > ema50 and rsi < 30:
        return f"BUY LONG {symbol} at {current_price:.4f} | EMA20: {ema20:.4f}, EMA50: {ema50:.4f}, RSI: {rsi:.2f}"
    elif current_price < ema20 < ema50 and rsi > 70:
        return f"SELL SHORT {symbol} at {current_price:.4f} | EMA20: {ema20:.4f}, EMA50: {ema50:.4f}, RSI: {rsi:.2f}"
    return None

def main():
    symbols = ["ETHUSDT", "GUNUSDT", "XRPUSDT"]
    for symbol in symbols:
        closes = get_klines(symbol)
        if closes:
            signal = generate_signal(symbol, closes)
            if signal:
                send_to_telegram(signal)
            else:
                print(f"No valid signal for {symbol}")
        else:
            print(f"Skipping {symbol} due to missing candle data.")

if __name__ == "__main__":
    main()
