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


if __name__ == "__main__":
    updater = telegram.ext.Updater(
        token=TELEGRAM_API_TOKEN,
        use_context=True)
    updater.start_polling()
