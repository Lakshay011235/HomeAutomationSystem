from socket import *
from helper import *
import json

# Logging configurations
import logging
import logging.config
logging.config.dictConfig(json.load(open('loggingConfig.json', 'r')))


def createServer():
    if(isPortAvailable == False):
        print("The given port is not available at this host")
        print("Please, try a different port or host address")
        return False
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        serverSocket.bind((HOST_ADDRESS, PORT_ADDRESS))
        
    except Exception as e:
        logging.exception("Error in server")
        
    serverSocket.close()

if __name__ == "__main__":
    # createServer()
    print(isPortAvailable(HOST_ADDRESS, PORT_ADDRESS))    
    # logging.debug(createServer())
    
    