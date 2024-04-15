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

    def send(self, msg):
        """
        Sends a message to the connected server. \n
        And receives the response from the server

        Parameters
        ----------
        msg : str
            A string containing the message to be sent.

        Returns
        -------
        response : dict
            Response from the server. __Message protocol version 1.0__\n
            ```
            {
            'responseCode' : responseCode,
            'message' : responseMessage
            }
            ```
        """
        packet = encodeMessagePacket(msg, HEADER_SIZE, FORMAT)
        self._clientSocket.send(packet)
        response = decodeResponsePacket(self._clientSocket.recv(2048))
        self.history.append(response)
        return response

    def close(self):
        """
        Closes the client's connection to the server.
        """
        self._clientSocket.close()
    
# client1 = Client()
# client1.send("Hello, world!")
# # # asdf = str(input())
# # send("Second message")
# # # input()
# # client1.send("CLOSE_SERVER")
# client1.send(DISCONNECT_MESSAGE)

