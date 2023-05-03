import os
import json
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from kafka import KafkaConsumer

# Load environment variables from the .env file
load_dotenv()

# Read environment variables for Database Connection
CLIENT = MongoClient(os.getenv("mongodbUri"))
DB = CLIENT[os.getenv("db_name")]
DEVICE_DATA = DB[os.getenv("data_stream_collection")]

# Read environment variables for topic name and bootstrap servers
TOPIC_NAME = os.getenv("topic_name")
BOOTSTRAP_SERVERS = os.getenv("bootstrap_servers")

try:
    # KafkaConsumer object
    CONSUMER = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BOOTSTRAP_SERVERS, api_version=(0,11,5), auto_offset_reset='latest')
    
    # Looping through the data received from Kafka topic
    for DATA in CONSUMER:
        try:
            # Parse the JSON data 
            DATA = json.loads(DATA.value)
            if not DATA:
                break
            # Insert data into MongoDB
            data = DEVICE_DATA.insert_one(DATA)
            print(DATA)
        except json.decoder.JSONDecodeError:
            continue

except KeyboardInterrupt:
    sys.exit()
