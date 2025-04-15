import requests
import time
import datetime

# Telegram Bot Config
TOKEN = '7744317479:AAGWhMOivMNuDwU5iCp4pAYf3lx50YFU-Aw'
CHANNEL = '@samir80s'

# Coin list
COINS = ['XRPUSDT', 'TRXUSDT', 'LINKUSDT', 'ZECUSDT']
TIMEFRAMES = ['15m', '30m']

# Binance API endpoint
def get_klines(symbol, interval, limit=100):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return None

# Support and Resistance calculation
def calculate_levels(data):
    closes = [float(x[4]) for x in data]
    support = min(closes)
    resistance = max(closes)
    return support, resistance

# Price breakout logic
def check_breakout(symbol, interval):
    data = get_klines(symbol, interval)
    if not data:
        return None

    support, resistance = calculate_levels(data)
    current_price = float(data[-1][4])
    price_change = (current_price - float(data[-2][4])) / float(data[-2][4]) * 100

    # Ignore small signals
    if abs(price_change) < 1.2:
        return None

    if current_price > resistance * 1.003:
        signal_type = 'BUY LONG'
        sl = round(current_price * 0.985, 4)
        tp = round(current_price * 1.025, 4)
    elif current_price < support * 0.997:
        signal_type = 'SELL SHORT'
        sl = round(current_price * 1.015, 4)
        tp = round(current_price * 0.975, 4)
    else:
        return None

    return {
        'symbol': symbol,
        'price': current_price,
        'support': support,
        'resistance': resistance,
        'signal': signal_type,
        'stop_loss': sl,
        'take_profit': tp,
        'interval': interval
    }

# Send message to Telegram
def send_telegram(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHANNEL,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=data)

# Run bot
def run_bot():
    while True:
        for symbol in COINS:
            for tf in TIMEFRAMES:
                signal = check_breakout(symbol, tf)
                if signal:
                    msg = f"""
*Signal Alert - {signal['symbol']} ({signal['interval']})*

*Type:* {signal['signal']}
*Price:* {signal['price']}
*Support:* {signal['support']}
*Resistance:* {signal['resistance']}
*Stop Loss:* {signal['stop_loss']}
*Take Profit:* {signal['take_profit']}
*Time:* {datetime.datetime.now().strftime('%H:%M:%S')}
"""
                    send_telegram(msg)
                else:
                    print(f"{symbol} {tf} - No strong signal, waiting...")

        time.sleep(900)  # 15 minutes wait

if __name__ == '__main__':
    run_bot()
