import requests
import time

BOT_TOKEN = '7744317479:AAGWhMOivMNuDwU5iCp4pAYf3lx50YFU-Aw'
CHANNEL_USERNAME = '@samir80s'
PAIRS = ['ETHUSDT', 'BTCUSDT', 'XRPUSDT']

def get_price(pair):
    try:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
        res = requests.get(url, timeout=10)
        data = res.json()
        if 'price' in data:
            return float(data['price'])
        else:
            return None
    except Exception as e:
        print(f"Error fetching price for {pair}: {e}")
        return None

def generate_signal():
    message = "Crypto Signal Queen Update:\n\n"
    for pair in PAIRS:
        price = get_price(pair)
        if price is None:
            message += f"⚠️ {pair}: *Error fetching price*\n"
            continue

        if str(price).endswith('.00'):
            signal = "Buy Long"
            emoji = "🟢"
            sl = round(price * 0.98, 2)
            tp = round(price * 1.02, 2)
        elif str(price).endswith('.50'):
            signal = "Sell Short"
            emoji = "🔴"
            sl = round(price * 1.02, 2)
            tp = round(price * 0.98, 2)
        else:
            signal = "Wait"
            emoji = "⏸️"
            sl = "-"
            tp = "-"

        message += (
            f"{emoji} *{pair}*\n"
            f"Signal: {signal}\n"
            f"Price: {price}\n"
            f"SL: {sl}\n"
            f"TP: {tp}\n\n"
        )
    return message

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHANNEL_USERNAME,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        res = requests.post(url, data=payload)
        print(res.text)
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == '__main__':
    signal_message = generate_signal()
    send_telegram_message(signal_message)
