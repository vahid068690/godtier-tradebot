import requests
import time
from datetime import datetime
from telegram import Bot
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

def rsi(prices, period=14):
    delta = np.diff(prices)
    up = delta.clip(min=0)
    down = -1 * delta.clip(max=0)
    avg_gain = np.convolve(up, np.ones(period)/period, mode='valid')[-1]
    avg_loss = np.convolve(down, np.ones(period)/period, mode='valid')[-1]
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))

def sma(prices, period):
    return np.mean(prices[-period:])

def analyze(symbol):
    prices, volumes = get_klines(symbol)
    rsi_val = rsi(prices)
    ma_fast = sma(prices, 5)
    ma_slow = sma(prices, 20)
    vol_avg = np.mean(volumes[-10:])
    vol_now = volumes[-1]
    signal = None

    if rsi_val < 30 and ma_fast > ma_slow and vol_now > 1.5 * vol_avg:
        signal = "سیگنال خرید (خروج نهنگ و فرصت احتمالی صعود)"
    elif rsi_val > 70 and ma_fast < ma_slow and vol_now > 1.5 * vol_avg:
        signal = "سیگنال فروش (ورود نهنگ و فشار فروش بالا)"
    return signal, prices[-1], rsi_val

def send_signal(symbol, message, price, rsi_val):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"📡 سیگنال God-Tier AI\n⏱ {now}\n📊 نماد: {symbol}\n💵 قیمت: {price:.2f} USDT\n📈 RSI: {rsi_val:.2f}\n⚠️ وضعیت: {message}"
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
