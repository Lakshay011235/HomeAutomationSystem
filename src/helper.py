import socket

SERVER_HOST_ADDRESS = socket.gethostbyname(socket.gethostname())
SERVER_PORT_ADDRESS = 9090

# defines first message length in bytes
# used for setting future message lengths in bytes
HEADER_SIZE = 64

# default format used over internet connections
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "Disconnect"
DISCONNECT_TIMEOUT = 10 # seconds
DISCONNECT_TIMEOUT_INTERVAL = DISCONNECT_TIMEOUT // 4

# Server Status Codes
REQUEST_SUCCESS = 200
REQUEST_FAILURE = 400


def isPortAvailable(host : str, port: int) -> bool:
    """
    Checks if the given port is available or not.

    Parameters
    ----------
    host : str
        The host address or IP address.
    port : int
        The port number associated with the address.
    
    Returns
    -------
    bool
        True if the port is available.
        False if the port is not available.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((host, port))
        sock.close()
        return False
    except:
        return True


# ----------------------------------------------------------------
# MESSAGE PROTOCOL_VERSION 1.0
"""
    [message length: int][message: string]
"""

# TODO: Convert to a packet class

def encodeMessagePacket(msg, header_size=64, encoding='utf-8'):
    message = msg.encode(encoding)
    msgLength = len(message)
    sendLength = str(msgLength).encode(encoding)
    # pad length to header length
    sendLength += b' '*(header_size - len(sendLength))
    packet = sendLength + message
    return packet

def decodeMessagePacket(msg, header_size=64, encoding='utf-8'):
    msg = msg.decode(encoding)
    return(msg)

def encodeResponsePacket(response_code, response_message, encoding='utf-8'):
    response = f"[{response_code}]{response_message}"
    return response.encode(encoding)

def decodeResponsePacket(msg, header_size=64, encoding='utf-8'):
    msg = msg.decode(encoding)
    responseCode = int(msg[1:4])
    response = msg[5:]
    return {
        'responseCode': responseCode, 
        'message':response
        }

def makeMessagePacketV2():
    pass
