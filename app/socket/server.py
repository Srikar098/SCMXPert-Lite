import socket
import errno
import json
import time
import random


# Port number and address to bind the server socket
PORT = 8080
ADDR = ("", PORT)
FORMAT = 'utf-8'

# Socket object for the server
SOCKET_CONNECTION = socket.socket()
print("SOCKET CREATED")

# Bind the server socket to the specified address and port number
SOCKET_CONNECTION.bind(ADDR)
SOCKET_CONNECTION.listen(2)


try:
    # Accept the connection from the client
    client, addr = SOCKET_CONNECTION.accept()
    print(f'Connection from {addr} has been established')

    # Setting a flag to indicate that the server is connected to a client
    connected = True
    # Initialize counter variable
    counter = 0
    # Loop for 10 iterations
    while connected and counter < 10:
            
            try:
                route = ['Tirupati, India','Hyderabad, India','Mumbai, India','Bengaluru, India']
                routefrom = random.choice(route)
                routeto = random.choice(route)
                if (routefrom!=routeto):
                    # Dictionary of random data
                    data = {
                        "Battery_Level":round(random.uniform(2.00,5.00),2),
                        "Device_ID": random.randint(1150,1158),
                        "First_Sensor_Temperature":round(random.uniform(10,40.0),1),
                        "Route_From":routefrom,
                        "Route_To":routeto,
                        "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    # Encode the data as a JSON object and send it to the client
                    userdata = (json.dumps(data)+"\n").encode(FORMAT)
                    client.send(userdata)
                    print(userdata)
                    time.sleep(10) 
                else:
                    continue
                # Increment the counter
                counter += 1      
            except IOError as e:
                if e.errno == errno.EPIPE:
                    pass

finally:
    # Closing the client connection
    client.close()
    print("Connection closed")