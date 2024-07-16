import socket
from .helper import *

class Client:
    """
    Represents a client that connects to a server using TCP/IP socket communication.

    Attributes:
        _clientSocket: A socket object for client-server communication.
    """

    def __init__(self):
        """
        Initializes the client by creating a socket object and connecting to the server.
        """
        self._clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clientSocket.connect((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))
        self.history = []

    def send(self, msg="", packet = None):
        if not isinstance(packet, PacketTemplate):
            packet = PacketTemplate(body=Body(content=msg)).to_bytes()
        self._clientSocket.send(packet)
        response = PacketTemplate(self._clientSocket.recv(5000))
        self.history.append(response.to_dict())
        return response

    def close(self):
        """
        Closes the client's connection to the server.
        """
        self._clientSocket.close()
    
# client1 = Client()
# res = client1.send("Hello, world!")
# print(res.body.to_dict())
# # # asdf = str(input())
# # send("Second message")
# # # input()
# # client1.send("CLOSE_SERVER")
# client1.send(DISCONNECT_MESSAGE)

