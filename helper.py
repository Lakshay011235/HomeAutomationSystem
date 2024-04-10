import socket

HOST = '127.0.0.1'
PORT = 9090

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

