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

# import socket
# import threading

# # Create a socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('localhost', 8888))
# server_socket.listen(5)

# # Function to accept incoming connections
# def accept_connections():
#     while True:
#         client_socket, client_address = server_socket.accept()
#         print(f"Accepted connection from {client_address}")
#         client_socket.send(b"Hello from server!")
#         client_socket.close()  # Close the client socket immediately

# # Start the accepting thread
# accept_thread = threading.Thread(target=accept_connections)
# accept_thread.start()

# # Stop accepting new connections after some time
# # This will close the server socket and prevent new connections
# # Existing connections will continue until closed by the client or server
# import time
# time.sleep(10)  # Wait for 10 seconds
# server_socket.close()
# print("Server socket closed. No longer accepting new connections.")

from src.helper import isPortAvailable, SERVER_PORT_ADDRESS

print(isPortAvailable("localhost", SERVER_PORT_ADDRESS))