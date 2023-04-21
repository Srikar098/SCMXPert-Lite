import socket
import os
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

SOCKET_CONNECTION = socket.socket()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
TOPIC_NAME = os.getenv("topic_name")
BOOTSTRAP_SERVERS = os.getenv("bootstrap_servers")

try:
    SOCKET_CONNECTION.connect((HOST, int(PORT)))
    print("Socket connected successfully!")

    PRODUCER = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, retries=5)

    while True:
        try:
            DATA = SOCKET_CONNECTION.recv(70240)
            print(DATA)
            PRODUCER.send(TOPIC_NAME, DATA)

        except Exception as e:
            print(e)
            break

finally:
    SOCKET_CONNECTION.close()
    print("Socket connection closed.")

