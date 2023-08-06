"""
Configuration Class for Telegram Bot
"""

class TelegramConfig:
    """
    Configuration Variable for Telegram Bot

    Parameters
    ---
    bot_token: BOT TOKEN recieved from @botfather

    chat_id: CHAT ID received from https://api.telegram.org/bot{BOT_TOKEN}/getUpdates
    """
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id