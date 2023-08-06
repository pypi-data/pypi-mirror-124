"""
Tensorflow Callback for Telegram Notification
"""

import requests
import logging
from .config import TelegramConfig
from tensorflow import keras

logger = logging.getLogger("telegram-bot")

class TelegramCallback(keras.callbacks.Callback):
    """
    Tensorflow Callback for Telegram Notification

    Parameters
    ---
    config: TelegramConfig object
    train: Send notification at start and end of training
    test: Send notification at start and end of testing
    predict: Send notification at start and end of prediction
    epochs: Send notification at end of each epoch
    """
    def __init__(self, config: TelegramConfig, train:bool = True,
                 test:bool = True, predict:bool = True,
                 epochs:bool = False):
        super().__init__()
        self.bot_token = config.bot_token
        self.chat_id = config.chat_id

        # Save configurations
        self._on_train = train
        self._on_test = test
        self._on_predict = predict
        self._on_epoch = epochs

    def _notify(self, message:str):
        """
        Function to send a notification

        Parameters
        ---
        message: Message to send
        """
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&text="{message}"'
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(err)

    def on_train_begin(self, logs=None):
        if self._on_train:
            message = "Training Started\n"
            for key, value in logs.items():
                message += f"{key} : {value}\n"

            self._notify(message)
            logger.info("Starting training; Sent Notification")

    def on_train_end(self, logs=None):
        if self._on_train:
            message = "Training Completed\n"
            for key, value in logs.items():
                message += f"{key} : {value}\n"

            self._notify(message)
            logger.info("Completed training; Sent Notification")

    def on_test_begin(self, logs=None):
        if self._on_test:
            message = "Testing Started\n"
            for key, value in logs.items():
                message += f"{key} : {value}\n"

            self._notify(message)
            logger.info("Starting testing; Sent Notification")

    def on_test_end(self, logs=None):
        if self._on_test:
            message = "Testing Completed\n"
            for key, value in logs.items():
                message += f"{key} : {value}\n"

            self._notify(message)
            logger.info("Completed testing; Sent Notification")

    def on_predict_begin(self, logs=None):
        if self._on_predict:
            message = "Prediction Started\n"
            for key, value in logs.items():
                message += f"{key} : {value}\n"

            self._notify(message)
            logger.info("Starting prediction; Sent Notification")

    def on_predict_end(self, logs=None):
        if self._on_predict:
            message = "Prediction Completed\n"
            for key, value in logs.items():
                message += f"{key} : {value}\n"

            self._notify(message)
            logger.info("Completed prediction; Sent Notification")

    def on_epoch_end(self, epoch, logs=None):
        if self._on_epoch:
            message = f"Epoch: {epoch}\n"
            for key, value in logs.items():
                message += f"{key} : {value}\n"

            self._notify(message)