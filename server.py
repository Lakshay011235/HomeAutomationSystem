import socket
from helper import *
import json
import threading

# Logging configurations
import logging
import logging.config
logging.config.dictConfig(json.load(open('loggingConfig.json', 'r')))


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


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))

def handleClient(conn, addr):
    logging.info(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break
            print(f"[{addr}] : {msg}")
            logging.info(f"[MESSAGE RECEIVED] {addr} | {msgLength} | {msg}")
            conn.send("Msg Received".encode(FORMAT))

    conn.close()
    logging.warning(f"[REMOVED CONNECTION] {addr} disconnected.")
    logging.info(f"[ACTIVE CONNECTIONS] {threading.active_count()-2}")


def start():
    serverSocket.listen()
    logging.info(f"[LISTENING] server is listening on port {serverSocket.getsockname()}")
    while True:
        # conn = client socket object
        # addr = client address
        conn, addr  = serverSocket.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        logging.info(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

logging.info("[STARTING] server is starting...")
start()


# if __name__ == "__main__":
#     createServer()
#     print(HOST_ADDRESS)
#     print(isPortAvailable(SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))    
#     logging.debug(createServer())
    
    
# TODO: Add json serialization
# TODO: Add inter-client communication