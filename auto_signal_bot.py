import requests
import time
from datetime import datetime

# Replace with your actual bot token and channel username
TOKEN = '7744317479:AAGWhMOivMNuDwU5iCp4pAYf3lx50YFU-Aw'
CHANNEL_ID = '@samir80s'

def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    res = requests.get(url)
    return float(res.json()['price'])

def send_signal(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHANNEL_ID,
        'text': message
    }
    requests.post(url, data=data)

def generate_signal():
    pairs = ['ETHUSDT', 'XRPUSDT', 'GUNUSDT']
    for pair in pairs:
        price = get_price(pair)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Simple logic for demo (can be replaced with advanced trend logic)
        if pair == 'ETHUSDT' and price < 1600:
            signal = f'[{current_time}] BUY SIGNAL: {pair} at ${price}'
        elif pair == 'ETHUSDT' and price > 1800:
            signal = f'[{current_time}] SELL SIGNAL: {pair} at ${price}'
        elif pair == 'XRPUSDT' and price < 0.45:
            signal = f'[{current_time}] BUY SIGNAL: {pair} at ${price}'
        elif pair == 'XRPUSDT' and price > 0.55:
            signal = f'[{current_time}] SELL SIGNAL: {pair} at ${price}'
        elif pair == 'GUNUSDT' and price < 0.004:
            signal = f'[{current_time}] BUY SIGNAL: {pair} at ${price}'
        elif pair == 'GUNUSDT' and price > 0.006:
            signal = f'[{current_time}] SELL SIGNAL: {pair} at ${price}'
        else:
            signal = f'[{current_time}] {pair} price: ${price} – No clear signal'

        send_signal(signal)

# Main runner
generate_signal()
