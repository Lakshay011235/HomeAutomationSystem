# import struct

# # Define the data to pack
# data1 = 1234
# data2 = b'ABCD'

# # Pack the data using different format specifiers
# packed_data1 = struct.pack('H', data1)  # Pack data1 as a 2-byte unsigned short
# packed_data2 = struct.pack('4s', data2)  # Pack data2 as a 4-byte string

# # Join the packed data into a single byte sequence
# joined_data = packed_data1 + packed_data2

# print(joined_data)  # This will print the byte sequence containing both packed data1 and packed data2

# # Separate the joined data back into their original forms
# unpacked_data1 = struct.unpack('H', joined_data[:2])[0]  # Unpack the first 2 bytes as an unsigned short
# unpacked_data2 = struct.unpack('4s', joined_data[2:])[0]  # Unpack the remaining bytes as a string

# print(unpacked_data1)  # This will print the unpacked data1 (1234)
# print(unpacked_data2.decode('utf-8'))  # This will print the unpacked data2 (ABCD)

# from src.helper import isPortAvailable, SERVER_PORT_ADDRESS

# print(isPortAvailable("localhost", SERVER_PORT_ADDRESS))

import threading
import time
from src.server import Server
from src.client import Client

from src.helper import *
a = PacketTemplate(header=Header(content="ASDFASDFASDf"), body=Body(content="ASDFASDf"))
# c = PacketTemplate.from_dict(a.to_dict())

# print(f"|{c.header.protocol_version}|")
# print(f"|{c.header.enc_type}|")
# print(f"|{c.header.public_key}|")
# print(f"|{c.header.encoding}|")
# print(f"|{c.header.content}|")
# print(f"|{c.body.content}|")


server = Server()
server_thread = threading.Thread(target=server.start)
server_thread.start()

def test():
    client = Client()

    response1 = client.send(a)
    print(response1.header.content)

    response2 = client.send(input())
    print(response2.header.content)
    response2 = client.send(input())
    print(response2.header.content)

    response3 = client.send("Disconnect")
    print(response3.header.content)

    # print(client.history)
    client.close()

c1 = threading.Thread(target=test)
c2 = threading.Thread(target=test)
c1.start()
c2.start()

for thread in threading.enumerate():
    if thread != threading.current_thread():
        thread.join()
        
        


# To close the server
# server._startAutoCloseTimer()