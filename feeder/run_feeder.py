import os
import sys

from pyail import PyAIL

FEEDER_UUID = os.getenv('FEEDER_UUID')
FEEDER_NAME = os.getenv('FEEDER_NAME')

AIL_URL = os.getenv('AIL_URL')
AIL_KEY = os.getenv('AIL_KEY')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

try:
    pyail = PyAIL(AIL_URL, AIL_KEY, ssl=False)
    print("Hello World!")
except Exception as e:
    print(e)
    sys.exit(0)

data = 'my item content'
metadata = {}
source = FEEDER_NAME
source_uuid = FEEDER_UUID

pyail.feed_json_item(data, metadata, source, source_uuid)