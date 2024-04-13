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
    
    # serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # try:
    #     serverSocket.bind((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))
        
    # except Exception as e:
    #     logging.exception("Error in server")
        
    # serverSocket.close()




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
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))
        self.connections = {}
        self.isRunning = False
        self.isClosing = False
        self.autoCloseTimer = None
        self.idleMessenger = None
    
    def handleClient(self, conn, addr):
        logging.info(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        
        if connected:
            self.resetAutoCloseTimer()
            
        while connected:
            # print(decodeMessagePacket(conn.recv(5000)))
            
            msgLength = conn.recv(HEADER_SIZE).decode(FORMAT)
            if msgLength:
                msgLength = int(msgLength)
                msg = conn.recv(msgLength).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                # Save client data
                self.saveClientData(addr, msg)
                
                logging.info(f"[MESSAGE RECEIVED] {addr} | {msgLength} | {msg}")
                conn.send(encodeResponsePacket(REQUEST_SUCCESS, msg))
            else:
                conn.send(encodeResponsePacket(REQUEST_FAILURE, "Could not connect to server"))

        conn.close()
        self.connections.pop(addr)
        logging.warning(f"[REMOVED CONNECTION] {addr} disconnected.")
        logging.info(f"[ACTIVE CONNECTIONS] {len(self.connections)}")

        # Check if all connections are closed and start auto-close timer if needed
        if len(self.connections) == 0:
            self.isClosing = True
            self.startAutoCloseTimer()


    def saveClientData(self, addr, msg):
        # Add time to msg
        if addr in self.connections:
            self.connections[addr].append(msg)
        else:
            self.connections[addr] = [msg]
            
    def start(self):
        logging.info("[STARTING] server is starting...")
        self.serverSocket.listen()
        logging.info(f"[LISTENING] server is listening on port {self.serverSocket.getsockname()}")
        self.isRunning = True
        while self.isRunning:
            try:
                # conn = client socket object
                # addr = client address
                conn, addr  = self.serverSocket.accept()
                
                # Stop the server autoClose and IDLE messages
                self.isClosing = False
                
                # Create a thread for each client-connection
                thread = threading.Thread(target=self.handleClient, args=(conn, addr))
                thread.start()
                logging.info(f"[ACTIVE CONNECTIONS] {len(self.connections)+1}")
                
            except OSError as e:
                if self.isRunning:
                    logging.error("[SERVER ERROR] OSError | Error in accepting connection")
        
    def shutdown(self):
        try:
            self.serverSocket.close()
            # Wait for all client threads to finish
            for thread in threading.enumerate():
                if thread != threading.current_thread():
                    thread.join()
            logging.critical("[SERVER CLOSED]")
        except Exception as e:
            logging.exception(f"[SERVER ERROR] {type(e).__name__}")
        
    def startAutoCloseTimer(self):
        self.autoCloseTimer = threading.Timer(DISCONNECT_TIMEOUT+1, self.checkAndClose)
        self.idleMessenger = threading.Thread(target=self.idleMessage)
        self.autoCloseTimer.start()
        self.idleMessenger.start()
        self.isClosing = True
        
    def resetAutoCloseTimer(self):
        self.isClosing = False
        if self.autoCloseTimer:
            self.autoCloseTimer.cancel()
        if self.idleMessenger:
            self.idleMessenger.join()
            
    def idleMessage(self):
        timer = DISCONNECT_TIMEOUT
        while self.isClosing and timer > 0:
            print(f"INFO     |      [SERVER IDLE] Closing in {timer} seconds")
            timer -= DISCONNECT_TIMEOUT//4
            time.sleep(DISCONNECT_TIMEOUT//4)

    # TODO: Make me daemon thread
    def checkAndClose(self):
        if len(self.connections) == 0 and self.isClosing == True:
            self.isRunning = False
            self.shutdown()
        else:
            pass
        # else:
        #     # Restart the auto-close timer
        #     self.startAutoCloseTimer()
    
# TODO: Add json serialization
# TODO: Add inter-client communication

server1 = Server()
server1.start()