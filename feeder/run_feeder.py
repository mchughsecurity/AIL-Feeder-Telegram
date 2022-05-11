import os
import sys
import redis
import logging
from pyail import PyAIL
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

from telethon.tl.types import Channel, User, ChannelParticipantsAdmins, PeerUser, PeerChat, PeerChannel
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl, MessageEntityMention
from telethon.tl.types import Chat, ChatEmpty
from telethon.tl.types import ChatInvite, ChatInviteAlready  # , ChatInvitePeek
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import CheckChatInviteRequest

from telethon.errors.rpcerrorlist import ChatAdminRequiredError, UserNotParticipantError
from telethon.errors.rpcerrorlist import InviteHashExpiredError, InviteHashInvalidError
from telethon.errors.common import MultiError


class TelegramFeeder:
    def __init__(self):
        self.FEEDER_UUID = os.getenv('FEEDER_UUID')
        self.FEEDER_NAME = os.getenv('FEEDER_NAME')
        self.FEEDER_ENABLED = os.getenv('FEEDER_ENABLED')

        self.AIL_URL = os.getenv('AIL_URL')
        self.AIL_KEY = os.getenv('AIL_KEY')
        self.AIL_SSLVERIFY = os.getenv('AIL_SSLVERIFY')

        self.REDIS_HOST = os.getenv('REDIS_HOST')
        self.REDIS_PORT = os.getenv('REDIS_PORT')
        self.REDIS_DB = os.getenv('REDIS_DB')
        self.REDIS = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT, db=self.REDIS_DB)

        self.TELEGRAM_API = os.getenv('TELEGRAM_API')
        self.TELEGRAM_HASH = os.getenv('TELEGRAM_HASH')
        self.TELEGRAM_SESSION = os.getenv('TELEGRAM_SESSION')

        try:

            logging.info("Creating test payload...\n")
            test_payload = 'Test string being submitted to AIL via PyAIL';
            test_payload_meta = {'some_attribute': 'some value'}

            logging.info("Testing connection to AIL...\n")
            self.PYAIL = PyAIL(self.AIL_URL, self.AIL_KEY, ssl=False)

            logging.info("Sending TEST payload {} with API Key {}. SSL Verify {}.\n".format(self.AIL_URL, self.AIL_KEY,
                                                                                            self.AIL_SSLVERIFY))

            # Send the test payload to AIL
            self.send_to_ail(data=test_payload, meta=test_payload_meta)

        except Exception as e:
            print(e)
            sys.exit(0)

    def connect_telegram(self):
        self.TELEGRAM = TelegramClient(self.TELEGRAM_SESSION, self.TELEGRAM_API, self.TELEGRAM_HASH)
        self.TELEGRAM.start()
        if not self.TELEGRAM.is_connected():
            logging.info("Telegram connection error!\n")
            sys.exit(0)
        return

    async def get_active_channels(self):
        active_channels = []
        async for dialog_obj in self.TELEGRAM.iter_dialogs():
            if not dialog_obj.is_user:
                channel_id = dialog_obj.id
                active_channels.append(channel_id)
        return active_channels

    async def get_channel_admins(self, channel):
        try:
            channel_admins = []
            async for user in self.TELEGRAM.iter_participants(channel, filter=ChannelParticipantsAdmins):
                channel_admins.append(user)
        except ChatAdminRequiredError:
            print(f'Error, {channel}: Chat admin privileges required')
        return channel_admins

    async def get_channel_users(self, channel):
        return

    async def get_channel_messages(self):
        return

    def construct_item_text(self, type, tags, text):
        ail_data = {
            'type': type,
            'tags': tags,
            'text': text
        }
        return ail_data

    def send_to_ail(self, data, meta):
        try:
            response = self.PYAIL.feed_json_item(
                data=data,
                meta=meta,
                source=self.FEEDER_NAME,
                source_uuid=self.FEEDER_UUID
            )
            logging.info("Packet has been sent to AIL\n")
        except Exception as e:
            print(e)
            sys.exit(0)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%I:%M:%S')
    Feeder = TelegramFeeder()

    # TODO: Check for the existence of a session file, if exists, use it for authentication.

    Feeder.connect_telegram()
    if Feeder.TELEGRAM.is_connected():
        logging.info("Telegram is connected.\n")
        # TODO: Check for session file, and save from this session if it does not exist.