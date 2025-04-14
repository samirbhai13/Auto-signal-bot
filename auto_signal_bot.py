import requests

BOT_TOKEN = '7744317479:AAGWhMOivMNuDwU5iCp4pAYf3lx50YFU-Aw'
CHANNEL_USERNAME = '@samir80s'
PAIRS = ['ETHUSDT', 'XRPUSDT', 'BTCUSDT']

def get_price(pair):
    try:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
        res = requests.get(url, timeout=10)
        data = res.json()
        return float(data['price']) if 'price' in data else None
    except Exception as e:
        print(f"Error fetching {pair}: {e}")
        return None

def generate_signal():
    message = "🔥 Crypto Signal Update 🔥\n\n"
    for pair in PAIRS:
        price = get_price(pair)
        if price is None:
            message += f"{pair}: ❌ Error fetching price\n"
            continue

        if str(price).endswith('.00'):
            signal = "🟢 Buy Long"
            sl = round(price * 0.99, 2)
            tp = round(price * 1.02, 2)
        elif str(price).endswith('.50'):
            signal = "🔴 Sell Short"
            sl = round(price * 1.01, 2)
            tp = round(price * 0.98, 2)
        else:
            signal = "⏳ Wait"
            sl = tp = "-"

        message += f"{pair} - {signal} at {price}\nSL: {sl} | TP: {tp}\n\n"
    return message

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHANNEL_USERNAME, 'text': message}
    try:
        res = requests.post(url, data=payload)
        print(res.text)
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == '__main__':
    msg = generate_signal()
    send_telegram_message(msg)
