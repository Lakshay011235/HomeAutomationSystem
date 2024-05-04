# import struct

# # Define the data to pack
# data1 = 1234
# data2 = b'ABCD'

# # Pack the data using different format specifiers
# packed_data1 = struct.pack('H', data1)  # Pack data1 as a 2-byte unsigned short
# packed_data2 = struct.pack('4s', data2)  # Pack data2 as a 4-byte string

# # Join the packed data into a single byte sequence
# joined_data = packed_data1 + packed_data2

# print(joined_data)  # This will print the byte sequence containing both packed data1 and packed data2

# # Separate the joined data back into their original forms
# unpacked_data1 = struct.unpack('H', joined_data[:2])[0]  # Unpack the first 2 bytes as an unsigned short
# unpacked_data2 = struct.unpack('4s', joined_data[2:])[0]  # Unpack the remaining bytes as a string

# print(unpacked_data1)  # This will print the unpacked data1 (1234)
# print(unpacked_data2.decode('utf-8'))  # This will print the unpacked data2 (ABCD)

# from src.helper import isPortAvailable, SERVER_PORT_ADDRESS

# print(isPortAvailable("localhost", SERVER_PORT_ADDRESS))

from abc import ABC, abstractmethod
import json

packet = {
    "head": {},
    "body": {}
}

# Custom Packet Parent
class PacketGod(ABC):
    def __init__(self, message, protocol):
        self.message = message
        self.protocol = protocol
        
    @abstractmethod
    def head(self):
        pass

    @abstractmethod
    def body(self):
        pass
    
    def protocol(self):
        return self.protocol
    
    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_data):
        data_dict = json.loads(json_data)
        return cls(**data_dict)
    
# Custom Packet
class GeneralPacket(PacketGod):
    def head(self):
        return self.message[:2]
    def body(self):
        return self.message[2:]

p1 = GeneralPacket("hello", "v1")

jp1 = p1.to_json()
print(jp1)

p2 = GeneralPacket.from_json(jp1)
print(p2.body())
