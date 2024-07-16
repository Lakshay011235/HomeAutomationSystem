import logging.config
import json
import pytest
import threading
import time
from src.server import Server
from src.client import Client

# # Temporarily set logging to print to console
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

with open('config/testLogConfig.json', 'r') as config_file:
    config = json.load(config_file)
    logging.config.dictConfig(config)

@pytest.fixture(scope="module")
def server():
    server = Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    yield server

@pytest.fixture(scope="module")
def client():
    client = Client()
    yield client
    client.close()
    
def test_my(server, client):
    start_time = time.time()
    response1 = client.send("Hellowwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")['responseCode']
    end_time = time.time()
    print(f"Time taken for test_my: {end_time - start_time} seconds")
    assert response1 == 200
    
def test_my2(server, client):
    start_time = time.time()
    response2 = client.send("Disconnect")['responseCode']
    end_time = time.time()
    logging.info(f"Time taken for test_my2: {end_time - start_time} seconds")
    assert response2 == 200
    