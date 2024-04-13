import socket

SERVER_HOST_ADDRESS = socket.gethostbyname(socket.gethostname())
SERVER_PORT_ADDRESS = 9090

# defines first message length in bytes
# used for setting future message lengths in bytes
HEADER = 64

# default format used over internet connections
FORMAT = 'utf-8'

DISCONNECT_TIMEOUT = 5000
DISCONNECT_MESSAGE = "Disconnect"

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

