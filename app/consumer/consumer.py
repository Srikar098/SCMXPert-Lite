import os
import json
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

CLIENT = MongoClient(os.getenv("mongodbUri"))
DB = CLIENT[os.getenv("db_name")]
DEVICE_DATA = DB[os.getenv("data_stream_collection")]

TOPIC_NAME = os.getenv("topic_name")
BOOTSTRAP_SERVERS = os.getenv("bootstrap_servers")

try:
    CONSUMER = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset='latest')
    for DATA in CONSUMER:
        try:
            DATA = json.loads(DATA.value)
            data = DEVICE_DATA.insert_one(DATA)
            print(DATA)
        except json.decoder.JSONDecodeError:
            continue
except KeyboardInterrupt:
    sys.exit()