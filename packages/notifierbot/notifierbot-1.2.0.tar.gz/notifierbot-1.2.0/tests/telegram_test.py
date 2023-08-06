import pytest
import requests

from notifierbot.telegram.bot import TelegramBot
from notifierbot.telegram.config import TelegramConfig
from notifierbot.telegram.tf_callback import TelegramCallback

def test_telegram_bot():
    config = TelegramConfig('', '')
    bot = TelegramBot(config)
    
    bot.add_message("Test Message")
    bot.notify()

def test_telegram_callback():
    config = TelegramConfig('', '')
    callback = TelegramCallback(config)
    
    callback.on_train_begin(logs = {"Error": 0.01})