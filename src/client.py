import socket
from .helper import *

class Client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))

    def send(self, msg):
        packet = encodeMessagePacket(msg, HEADER_SIZE, FORMAT)
        
        self.clientSocket.send(packet)
        
        response = decodeResponsePacket(self.clientSocket.recv(2048))
        print(response)
        return response
        
        
    
client1 = Client()
client1.send("Hello, world!")
# # asdf = str(input())
# send("Second message")
# # input()
# client1.send("CLOSE_SERVER")
client1.send(DISCONNECT_MESSAGE)

