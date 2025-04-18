import requests
import time

# Telegram Bot Config
BOT_TOKEN = "7744317479:MOivMNuDwU5iCp4pAYf3lx50YFU-Aw"
CHANNEL_ID = "@sa0s"

# Coin Pairs
SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "GUNUSDT"]

# Timeframes in minutes (for analysis info)
TIMEFRAMES = ["15m", "30m"]

# Telegram send function
def send_signal(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

# Price fetch function
def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=5)
        data = res.json()
        return float(data['price'])
    except:
        return None

# Signal generator (basic logic)
def generate_signal(symbol):
    price = get_price(symbol)
    if price is None:
        return f"*{symbol}*: Error fetching price, retry later."

    # Dummy logic for buy/sell signal (replace with real indicators later)
    if symbol == "BTCUSDT" and price < 64000:
        signal = "Buy Long"
        sl = round(price * 0.985, 2)
        tp = round(price * 1.025, 2)
        reason = "Price near support zone."
    elif symbol == "BTCUSDT" and price > 69000:
        signal = "Sell Short"
        sl = round(price * 1.015, 2)
        tp = round(price * 0.97, 2)
        reason = "Price near resistance zone."
    elif "USDT" in symbol:
        # Simple alternate logic for others
        if price % 2 < 1:
            signal = "Buy Long"
            sl = round(price * 0.985, 4)
            tp = round(price * 1.025, 4)
            reason = "Technical signal generated."
        else:
            signal = "Sell Short"
            sl = round(price * 1.015, 4)
            tp = round(price * 0.975, 4)
            reason = "Price reversal expected."
    else:
        return f"*{symbol}*: No signal."

    return f"""
*{symbol} {signal} Signal*

Entry Price: `{price}`
Stop Loss: `{sl}`
Take Profit: `{tp}`
Timeframes: {', '.join(TIMEFRAMES)}

_Analysis: {reason}_
"""

# Run for each symbol
if __name__ == "__main__":
    for symbol in SYMBOLS:
        message = generate_signal(symbol)
        send_signal(message)
        time.sleep(2)  # Delay to avoid Telegram flood
