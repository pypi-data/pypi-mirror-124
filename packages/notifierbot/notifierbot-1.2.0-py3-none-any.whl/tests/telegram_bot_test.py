import pytest
import requests

from notifierbot.telegram.bot import TelegramBot
from notifierbot.telegram.config import TelegramConfig

def test_telegram_bot():
    config = TelegramConfig('', '')
    bot = TelegramBot(config)
    
    bot.add_message("Test Message")
    bot.notify()