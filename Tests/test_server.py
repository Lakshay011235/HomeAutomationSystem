import logging.config
import json
import pytest
import threading
import time
from src.server import Server
from src.client import Client
from src.helper import SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS, HEADER_SIZE, FORMAT, DISCONNECT_MESSAGE

with open('Tests/serverLoggingConfig.json', 'r') as config_file:
    config = json.load(config_file)
    logging.config.dictConfig(config)

# Fixture to start and stop the server
@pytest.fixture(scope="module")
def server():
    server = Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    yield server
    server.shutdown()
    server_thread.join()

# Fixture to create a client
@pytest.fixture(scope="module")
def client():
    client = Client()
    return client

# Test basic server-client interaction
def test_server_client_interaction(server, client):
    client.send("Hello, server!")
    time.sleep(1)  # Wait for the message to be sent
    assert True  # If the test reaches this point without errors, it passed
    # logging.info(f"[{test_result}]")
    

