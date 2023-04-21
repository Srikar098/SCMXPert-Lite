import socket
import json
import time
import random
import datetime


PORT = 8080
FORMAT = 'utf-8'

SOCKET_CONNECTION = socket.socket()
print("Socket Created")
SOCKET_CONNECTION.bind(('',int(PORT)))
SOCKET_CONNECTION.listen(3)



while True:
    client, addr = SOCKET_CONNECTION.accept()
    print("connected with", addr)
    try:
        for i in range(0,5):
            route = ['Tirupati, India','Hyderabad, India','Mumbai, India','Bengaluru, India']
            routefrom = random.choice(route)
            routeto = random.choice(route)
            if (routefrom!=routeto):
                data = {
                    "Device_ID": random.randint(110356,110450),
                    "Battery_Level":round(random.uniform(2.00,5.00),2),
                    "First_Sensor_Temperature":round(random.uniform(10,40.0),1),
                    "Route_From":routefrom,
                    "Route_To":routeto
                    }
                userdata = (json.dumps(data, indent=1)).encode(FORMAT)
                client.send(userdata)
                print(userdata)
                time.sleep(10)
            else:
                continue                       
    except Exception as e:
        print(e)
    client.close()