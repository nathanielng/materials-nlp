#!/usr/bin/env python

# Requirements:
# pip install python-telegram-bot

import logging
import os
import telegram.ext


# Setup API Keys
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')


# Setup Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update, ctx):
    ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Bot is ready"
    )


if __name__ == "__main__":
    updater = telegram.ext.Updater(token=TELEGRAM_API_TOKEN, use_context=True)
    h_start = telegram.ext.CommandHandler('start', start)
    updater.dispatcher.add_handler(h_start)
    updater.start_polling()
