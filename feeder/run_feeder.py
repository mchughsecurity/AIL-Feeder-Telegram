import json
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

FEEDER_UUID = os.getenv('FEEDER_UUID')
FEEDER_NAME = os.getenv('FEEDER_NAME')
FEEDER_ENABLED = os.getenv('FEEDER_ENABLED')

AIL_URL = os.getenv('AIL_URL')
AIL_KEY = os.getenv('AIL_KEY')
AIL_SSLVERIFY = os.getenv('AIL_SSLVERIFY')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

TELEGRAM_API = os.getenv('TELEGRAM_API')
TELEGRAM_HASH = os.getenv('TELEGRAM_HASH')
TELEGRAM_SESSION = os.getenv('TELEGRAM_SESSION')

PYAIL = PyAIL(AIL_URL, AIL_KEY, ssl=False)
REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
TELEGRAM = TelegramClient(TELEGRAM_SESSION, TELEGRAM_API, TELEGRAM_HASH)

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%I:%M:%S')


async def main():
    # me = await TELEGRAM.get_me()

    # Get Active Channels
    async for conversation in TELEGRAM.iter_dialogs():
        print(conversation.name, 'has ID', conversation.id, '\n')

        # Get Messages from Active Channels
        async for message in TELEGRAM.iter_messages(entity=conversation.id):
            message_id = FEEDER_NAME + '-' + str(conversation.id) + '-' + str(message.id)
            message_link = 'https://t.me/' + conversation.entity.username + '/' + str(message.id)

            # Create meta-data for Telegram Message
            message_meta = {
                'telegram:message_id': message.id,
                'telegram:conversation_id': conversation.id,
                'telegram:message_datetime': message.date.strftime('%d/%m/%Y %H:%M:%S %Z'),
                'telegram:conversation': conversation.entity.username,
                'telegram:message_link': message_link
            }
            # print(json_message)

            # Check the Redis cache
            if REDIS.exists("c:{}".format(message_id)):
                print(message_id + ' already exists in Redis.')
                # sys.exit(0)
            else:
                # Set in Redis and send to AIL
                try:
                    REDIS.set("c:{}".format(message_id), message.text)
                    REDIS.expire("c:{}".format(message_id), 3600)
                    print(message_id + ' has been added to Redis')

                    ail_response = PYAIL.feed_json_item(
                        data=message.text,
                        meta=message_meta,
                        source=FEEDER_NAME,
                        source_uuid=FEEDER_UUID
                    )

                    print(ail_response)
                except Exception as e:
                    print(e)
                    # sys.exit(0)


with TELEGRAM:
    TELEGRAM.loop.run_until_complete(main())
