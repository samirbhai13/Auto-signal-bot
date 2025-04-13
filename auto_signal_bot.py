
import requests
from datetime import datetime
import time

# Telegram bot token & channel ID
TOKEN = '7744317479:AAGWhMOivMNuDwU5iCp4pAYf3lx50YFU-Aw'
CHANNEL_ID = '@samir80s'

# Function to fetch current price
def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    res = requests.get(url)
    return float(res.json()['price'])

# Function to send signal to Telegram
def send_signal(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=data)

# Function to generate signal
def generate_signal(symbol):
    current_price = get_price(symbol)
    message = f"<b>{symbol} Signal</b>\n"
    message += f"Current Price: <b>{current_price}</b>\n"
    
    # Example trend-based logic (can be customized)
    if symbol == 'ETHUSDT':
        if current_price <= 1560:
            message += "Buy Long Target: 1600, SL: 1530"
        elif current_price >= 1620:
            message += "Sell Short Target: 1580, SL: 1650"
        else:
            return  # No signal if price is not in range
    
    elif symbol == 'GUNUSDT':
        if current_price <= 0.019:
            message += "Buy Long Target: 0.022, SL: 0.017"
        elif current_price >= 0.024:
            message += "Sell Short Target: 0.021, SL: 0.026"
        else:
            return
    
    elif symbol == 'XRPUSDT':
        if current_price <= 0.52:
            message += "Buy Long Target: 0.56, SL: 0.50"
        elif current_price >= 0.60:
            message += "Sell Short Target: 0.56, SL: 0.63"
        else:
            return
    
    send_signal(message)

# Run signals for all tokens
def run_bot():
    symbols = ['ETHUSDT', 'GUNUSDT', 'XRPUSDT']
    for symbol in symbols:
        generate_signal(symbol)

# Main loop (used in GitHub Actions scheduler every 15min)
if __name__ == '__main__':
    run_bot()
