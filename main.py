import requests
import time
from datetime import datetime
from telegram import Bot
import talib
import numpy as np

TELEGRAM_TOKEN = "7917361837:AAFdjJ1l_VSTx-i1Oudolav2-pp0h079TLM"
CHANNEL_ID = -1002098489700
USER_ID = 96070970

bot = Bot(token=TELEGRAM_TOKEN)

def get_klines(symbol="BTCUSDT", interval="5m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    closes = [float(kline[4]) for kline in data]
    volumes = [float(kline[5]) for kline in data]
    return np.array(closes), np.array(volumes)

def analyze(symbol):
    prices, volumes = get_klines(symbol)
    rsi = talib.RSI(prices, timeperiod=14)[-1]
    ma_fast = talib.SMA(prices, timeperiod=5)[-1]
    ma_slow = talib.SMA(prices, timeperiod=20)[-1]
    vol_avg = np.mean(volumes[-10:])
    vol_now = volumes[-1]
    signal = None

    if rsi < 30 and ma_fast > ma_slow and vol_now > 1.5 * vol_avg:
        signal = "سیگنال خرید (خروج نهنگ و فرصت احتمالی صعود)"
    elif rsi > 70 and ma_fast < ma_slow and vol_now > 1.5 * vol_avg:
        signal = "سیگنال فروش (ورود نهنگ و فشار فروش بالا)"
    return signal, prices[-1], rsi

def send_signal(symbol, message, price, rsi):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"سیگنال هوشمند God-Tier\\nزمان: {now}\\nنماد: {symbol}\\nقیمت لحظه ای: {price:.2f} USDT\\nRSI: {rsi:.2f}\\nوضعیت: {message}"
    bot.send_message(chat_id=CHANNEL_ID, text=msg)
    bot.send_message(chat_id=USER_ID, text=msg)

def main_loop():
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
               "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT", "DOTUSDT"]
    while True:
        for symbol in symbols:
            try:
                result = analyze(symbol)
                if result[0]:
                    send_signal(symbol, *result)
            except Exception as e:
                print(f"خطا در پردازش {symbol}: {e}")
        time.sleep(300)

if __name__ == "__main__":
    main_loop()
