import socket
from helper import *


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    
    # pad length to HEADER length
    sendLength += b' '*(HEADER - len(sendLength))
    
    clientSocket.send(sendLength)
    clientSocket.send(message)
    
    print(clientSocket.recv(2048).decode(FORMAT))
    
    
send("Hello, world!")
asdf = str(input())
send(asdf)
input()
send(DISCONNECT_MESSAGE)