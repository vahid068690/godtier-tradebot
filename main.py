import requests
import time
from datetime import datetime
from telegram import Bot

TELEGRAM_TOKEN = "7917361837:AAFdjJ1l_VSTx-i1Oudolav2-pp0h079TLM"
CHANNEL_ID = "https://t.me/+BkeqKTzy3KlkYjk8"
USER_ID = 96070970  # آی‌دی شخصی شما

bot = Bot(token=TELEGRAM_TOKEN)

def get_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()["price"])

def send_signal(message):
    bot.send_message(chat_id=CHANNEL_ID, text=message)
    bot.send_message(chat_id=USER_ID, text=message)

def main_loop():
    while True:
        price = get_price()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"📈 سیگنال تست\n🕒 {now}\n💰 BTC/USDT: {price:.2f}\n📡 وضعیت: پایلوت فعال"
        send_signal(msg)
        time.sleep(300)  # هر ۵ دقیقه یک بار

if __name__ == "__main__":
    main_loop()
