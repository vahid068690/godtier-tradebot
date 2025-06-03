import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# توکن ربات
TOKEN = "7917361837:AAFdjJ1l_VSTx-i1Oudolav2-pp0h079TLM"

def start(update, context):
    update.message.reply_text("ربات God-Tier با موفقیت اجرا شد ✅")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
