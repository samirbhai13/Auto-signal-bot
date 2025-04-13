import requests
import time

# Telegram bot token and channel username
BOT_TOKEN = '7744317479:AAGWhMOivMNuDwU5iCp4pAYf3lx50YFU-Aw'
CHANNEL_USERNAME = '@samir80s'

# Crypto pairs to check
PAIRS = ['ETHUSDT', 'XRPUSDT', 'BTCUSDT']

# Signal conditions
def get_price(pair):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
    try:
        res = requests.get(url)
        data = res.json()
        if 'price' in data:
            return float(data['price'])
        else:
            print(f"Error fetching price for {pair}: {data}")
            return None
    except Exception as e:
        print(f"Exception fetching price: {e}")
        return None

def generate_signal():
    message = "🔥 *Crypto Signal Update* 🔥\n\n"
    for pair in PAIRS:
        price = get_price(pair)
        if price is None:
            message += f"{pair}: ❌ *Error fetching price*\n"
            continue

        # Simple logic: if price ends in .00, suggest long; if .50, suggest short
        if str(price).endswith('.00'):
            signal = "🟢 *Buy Long*"
            sl = round(price * 0.98, 2)
            tp = round(price * 1.02, 2)
        elif str(price).endswith('.50'):
            signal = "🔴 *Sell Short*"
            sl = round(price * 1.02, 2)
            tp = round(price * 0.98, 2)
        else:
            signal = "⏸️ *Wait*"
            sl = tp = None

        message += f"*{pair}* - {signal} at `{price}`\n"
        if sl and tp:
            message += f"➖ SL: `{sl}` | 🎯 TP: `{tp}`\n"
        message += "\n"
    return message

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHANNEL_USERNAME,
        'text': message,
        'parse_mode': 'Markdown'
    }
    res = requests.post(url, data=payload)
    print(res.text)

if __name__ == '__main__':
    signal_message = generate_signal()
    send_telegram_message(signal_message)
