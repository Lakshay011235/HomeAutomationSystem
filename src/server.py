import socket
from .helper import *
import json
import threading
import time

# Logging configurations
import logging
import logging.config
logging.config.dictConfig(json.load(open('config/loggingConfig.json', 'r')))

# def createServer():
    # if(isPortAvailable(SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS) == False):
    #     failResponse = "-"*60 + f"\nThe given port {(SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS)} is not available at this host" + "\nPlease, try a different port or host address\n" +"-"*60
    #     print(failResponse)
    #     return False
    
    # _serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # try:
    #     _serverSocket.bind((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))
        
    # except Exception as e:
    #     logging.exception("Error in server")
        
    # _serverSocket.close()




# MESSAGE PROTOCOL_VERSION 1.0
"""
    [message length: int][message: string]
"""

# TODO: MESSAGE PROTOCOL_VERSION 2.0
"""
    [protocol version][header length]
    [message length: int][message: string]
"""



# logging.info("[STARTING] server is starting...")
# start()

class Server:
    def __init__(self):
        self._serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serverSocket.bind((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))
        self._connections = {}
        self._isRunning = False
        self._isClosing = False
        self._autoCloseTimer = None
        self._idleMessenger = None
    
    def _handleClient(self, conn, addr):
        logging.warning(f"[NEW CONNECTION] {addr} connected.")
        self._connections[addr] = []
        connected = True
        
        if connected:
            self._resetAutoCloseTimer() 
            
        while connected:            
            packet = PacketTemplate(conn.recv(5000))
            if packet:
                if packet.body.content == DISCONNECT_MESSAGE:
                    connected = False

                # Implement version check
                
                # Save client data
                self._saveClientData(addr, packet.to_dict())
                
                logging.info(f"[MESSAGE RECEIVED] {addr} | {packet.body.content}")
                conn.send(PacketTemplate(header=Header(content=REQUEST_SUCCESS), body=Body(content=packet.body.content)).to_bytes())
            else:
                conn.send(PacketTemplate(header=Header(content=REQUEST_FAILURE), body=Body("Could not connect to server")).to_bytes())

        conn.close()
        self._connections.pop(addr)
        logging.warning(f"[REMOVED CONNECTION] {addr} disconnected.")
        logging.info(f"[ACTIVE CONNECTIONS] {len(self._connections)}")

        # Check if all _connections are closed and start auto-close timer if needed
        if len(self._connections) == 0 and not self._isClosing:
            self._isClosing = True
            self._startAutoCloseTimer()


    def _saveClientData(self, addr, msg):
        if addr in self._connections:
            self._connections[addr].append(msg)
            
    def start(self):
        logging.info("[STARTING] server is starting...")
        self._serverSocket.listen()
        logging.info(f"[LISTENING] server is listening on port {self._serverSocket.getsockname()}")
        self._isRunning = True
        while self._isRunning:
            try:
                # conn = client socket object
                # addr = client address
                conn, addr  = self._serverSocket.accept()
                
                # Stop the server autoClose and IDLE messages
                self._isClosing = False
                
                # Create a thread for each client-connection
                thread = threading.Thread(target=self._handleClient, args=(conn, addr))
                thread.start()
                logging.info(f"[ACTIVE CONNECTIONS] {len(self._connections)+1}")
                
            except OSError as e:
                if self._isRunning:
                    logging.exception("[SERVER ERROR] OSError | Error in accepting connection")
        
    def _shutdown(self):
        try:
            self._serverSocket.close()
            # Wait for all client threads to finish
            for thread in threading.enumerate():
                if thread != threading.current_thread():
                    thread.join()
            logging.critical("[SERVER CLOSED]")
        except Exception as e:
            logging.exception(f"[SERVER ERROR] {type(e).__name__}")
        
    def _startAutoCloseTimer(self):
        self._autoCloseTimer = threading.Timer(DISCONNECT_TIMEOUT+1, self._checkAndClose)
        self._idleMessenger = threading.Thread(target=self._idleMessage)
        self._autoCloseTimer.start()
        self._idleMessenger.start()
        self._isClosing = True
        
    def _resetAutoCloseTimer(self):
        self._isClosing = False
        if self._autoCloseTimer:
            self._autoCloseTimer.cancel()
        if self._idleMessenger:
            self._idleMessenger.join()
            
    def _idleMessage(self):
        timer = DISCONNECT_TIMEOUT
        while self._isClosing and timer > 0:
            logging.info(f"[SERVER IDLE] Closing in {timer} seconds")
            timer -= DISCONNECT_TIMEOUT//4
            time.sleep(DISCONNECT_TIMEOUT//4)

    # TODO: Make me daemon thread
    def _checkAndClose(self):
        if len(self._connections) == 0 and self._isClosing == True:
            self._isRunning = False
            self._shutdown()
        else:
            pass
    
# TODO: Add json serialization
# TODO: Add inter-client communication
# TODO: Add file sending

# server1 = Server()
# server1.start()

