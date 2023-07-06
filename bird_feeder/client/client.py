import socket
import logging
import threading
import queue

logging.basicConfig(
	level = logging.DEBUG,
	format = '[%(asctime)s] - %(message)s'
)

HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.connect((HOST, PORT))
    logging.info("Connected to server")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Client exiting")
except Exception:
    logging.error("Error occurred")