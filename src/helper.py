import socket

SERVER_HOST_ADDRESS = socket.gethostbyname(socket.gethostname())
SERVER_PORT_ADDRESS = 9090

# defines first message length in bytes
# used for setting future message lengths in bytes
HEADER_SIZE = 8

# default format used over internet connections
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "Disconnect"
DISCONNECT_TIMEOUT = 4 # seconds
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

# ----------------------------------------------------------------
# MESSAGE PROTOCOL_VERSION 2.0
# ----------------------------------------------------------------


class Header:
    def __init__(self, bytes_content=b'', content="", protocol_version="v1", enc_type="rsa", public_key="my_key", encoding="utf-8", header_size=8):
        self.__header_size = header_size
        self.__protocol_version = protocol_version
        self.__enc_type = enc_type
        self.__public_key = public_key
        self.__content = str(content)
        self.__encoding = encoding
        self.__length = str(len(self.__content))
        self.__container_sizes = tuple([x * self.__header_size for x in [1, 1, 1, 3]])
        if len(bytes_content) > 0:
            self.from_bytes(bytes_content)

    @property
    def length(self):
        return self.__length

    @property
    def protocol_version(self):
        return self.__protocol_version

    @protocol_version.setter
    def protocol_version(self, version):
        self.__protocol_version = version

    @property
    def enc_type(self):
        return self.__enc_type

    @enc_type.setter
    def enc_type(self, enc_type):
        self.__enc_type = enc_type

    @property
    def public_key(self):
        return self.__public_key

    @public_key.setter
    def public_key(self, key):
        self.__public_key = key

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, encoding):
        self.__encoding = encoding

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, new_content):
        self.__content = str(new_content)
        self.__length = str(len(self.__content))

    def _property_to_bytes(self, content, size):
        content = content.encode(self.encoding)
        if len(content) >= size:
            raise ValueError(f"Given content has [{len(content)}] is larger than the size handled [{size}] by the protocol")
        content += b' ' * (size - len(content))
        return bytes(content)

    def to_bytes(self):
        return (self._property_to_bytes(self.__length, self.__container_sizes[0])
                + self._property_to_bytes(self.__protocol_version, self.__container_sizes[1])
                + self._property_to_bytes(self.__enc_type, self.__container_sizes[2])
                + self._property_to_bytes(self.__public_key, self.__container_sizes[3])
                + bytes(self.__content, encoding=self.__encoding))

    def from_bytes(self, bytes_content):
        self.__length = bytes_content[0:self.__container_sizes[0]].decode(self.__encoding).strip()
        self.__protocol_version = bytes_content[self.__container_sizes[0]:self.__container_sizes[0] + self.__container_sizes[1]].decode(self.__encoding).strip()
        self.__enc_type = bytes_content[self.__container_sizes[0] + self.__container_sizes[1]:self.__container_sizes[0] + self.__container_sizes[1] + self.__container_sizes[2]].decode(self.__encoding).strip()
        self.__public_key = bytes_content[self.__container_sizes[0] + self.__container_sizes[1] + self.__container_sizes[2]:self.__container_sizes[0] + self.__container_sizes[1] + self.__container_sizes[2] + self.__container_sizes[3]].decode(self.__encoding).strip()
        self.__content = bytes_content[self.__container_sizes[0] + self.__container_sizes[1] + self.__container_sizes[2] + self.__container_sizes[3]:].decode(self.__encoding).strip()
        return self

    def to_dict(self):
        return {
            'protocol_version': self.__protocol_version,
            'enc_type': self.__enc_type,
            'public_key': self.__public_key,
            'content': self.__content,
            'encoding': self.__encoding,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            protocol_version=data['protocol_version'],
            enc_type=data['enc_type'],
            public_key=data['public_key'],
            content=data['content'],
            encoding=data['encoding'],
        )
class Body:    
    def __init__(self, bytes_content=b'', content="", encoding="utf-8", header_size=8):
        self.__header_size = header_size
        self.__content = str(content)
        self.__encoding = encoding
        self.__length = str(len(self.__content))
        if len(bytes_content) > 0:
            self.from_bytes(bytes_content)

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, new_content):
        self.__content = str(new_content)
        self.__length = str(len(self.__content))

    def _property_to_bytes(self, content, size):
        content = content.encode(self.__encoding)
        if len(content) >= size:
            raise ValueError(f"Given content has [{len(content)}] which is larger than the size handled [{size}] by the protocol")
        content += b' '*(size - len(content))
        return bytes(content)

    def to_bytes(self):
        return (self._property_to_bytes(self.__length, self.__header_size)
                + bytes(self.__content, encoding=self.__encoding))

    def from_bytes(self, bytes_content):
        self.__length = bytes_content[0:self.__header_size].decode(self.__encoding).strip()
        self.__content = bytes_content[self.__header_size:].decode(self.__encoding).strip()
        return self

    def to_dict(self):
        return {
            'content': self.__content,
            'encoding': self.__encoding,
            'length': self.__length
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            content=data['content'],
            encoding=data['encoding'],
        )

class PacketTemplate():
    def __init__(self, bytes_content = b'', header = Header(), body = Body()):
        self.body = body
        self.header = header
        if len(bytes_content) > 0:
            self.from_bytes(bytes_content)

    def to_bytes(self):
        return (self.header.to_bytes() + self.body.to_bytes())

    def from_bytes(self, bytes_content):
        self.header.from_bytes(bytes_content)
        self.body.from_bytes(bytes(self.header.content, encoding=self.header.encoding)[int(self.header.length):])
        self.header.content = self.header.content[:int(self.header.length)]
        return self

    def to_dict(self):
        return {
            'header': self.header.to_dict(),
            'body': self.body.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            header=Header.from_dict(data['header']),
            body=Body.from_dict(data['body'])
        )

    
# a = PacketTemplate(header=Header(content="ASDFASDFASDf"), body=Body(content="ASDFASDf"))
# c = PacketTemplate.from_dict(a.to_dict())

# print(f"|{c.header.protocol_version}|")
# print(f"|{c.header.enc_type}|")
# print(f"|{c.header.public_key}|")
# print(f"|{c.header.encoding}|")
# print(f"|{c.header.content}|")
# print(f"|{c.body.content}|")
