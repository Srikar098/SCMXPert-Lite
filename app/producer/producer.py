import socket
import os
from dotenv import load_dotenv
from kafka import KafkaProducer

# Load environment variables from the .env file
load_dotenv()

# Socket object for the server
SOCKET_CONNECTION = socket.socket()

# Read environment variables
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
TOPIC_NAME = os.getenv("topic_name")
BOOTSTRAP_SERVERS = os.getenv("bootstrap_servers")


try:
    # Connect to the remote host and port
    SOCKET_CONNECTION.connect((HOST, int(PORT)))
    print("Socket connected successfully!")

    # KafkaProducer object
    PRODUCER = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, retries=5)

    # Looping to read data from the socket connection and send it to the Kafka topic
    while True:
        try:
            DATA = SOCKET_CONNECTION.recv(70240)
            if not DATA:
                break
            print(DATA)
            # Send the data to the Kafka topic
            PRODUCER.send(TOPIC_NAME, DATA)

        except Exception as e:
            print(e)
            break

# Closing the socket connection
finally:
    SOCKET_CONNECTION.close()
    print("Socket connection closed.")

