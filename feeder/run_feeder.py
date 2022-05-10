import os
import sys

from telegram import *
from pyail import PyAIL


# data = 'my item content'
# metadata = {}
# source = FEEDER_NAME
# source_uuid = FEEDER_UUID

class TelegramFeeder:
    def __init__(self):
        self.FEEDER_UUID = os.getenv('FEEDER_UUID')
        self.FEEDER_NAME = os.getenv('FEEDER_NAME')
        self.FEEDER_ENABLED = os.getenv('FEEDER_ENABLED')
        self.AIL_URL = os.getenv('AIL_URL')
        self.AIL_KEY = os.getenv('AIL_KEY')
        self.AIL_SSLVERIFY = os.getenv('AIL_SSLVERIFY')
        try:
            self.AIL = PyAIL(self.AIL_URL, self.AIL_KEY, ssl=self.AIL_SSLVERIFY)
            print("AIL CONNECTED!\n")
        except Exception as e:
            print(e)
            sys.exit(0)

    def connect_to_telegram(self):
        try:
            self.TELEGRAM_API = os.getenv('TELEGRAM_API')
            self.TELEGRAM_HASH = os.getenv('TELEGRAM_HASH')
            self.TELEGRAM_SESSION = os.getenv('TELEGRAM_SESSION')
            self.TELEGRAM = TelegramClient(self.TELEGRAM_SESSION, self.TELEGRAM_API, self.TELEGRAM_HASH)
        except Exception as e:
            print("Could not authenticate to Telegram API.\n")
            sys.exit(0)

    def send_to_ail(self, data, metadata):
        try:
            self.AIL.feed_json_item(data, metadata, self.FEEDER_NAME, self.FEEDER_UUID)
            print("Message sent to AIL!\n")
        except Exception as e:
            print(e)
            sys.exit(0)


if __name__ == "__main__":
    Feeder = TelegramFeeder()
