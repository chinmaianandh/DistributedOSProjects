import socket
import argparse
import time
from common_utils import log_time

SERVER_ID = ("0.0.0.0", 8888)

def ping_server(SERVER_ID, client_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ID)

    print(f"{log_time()}\tSending Hello from {client_name}.")
    s.sendall(f"Hello from {client_name}!!".encode())

    data = s.recv(1024)

    print(f"{log_time()}\tReveived at {client_name} : {data.decode()}")

    s.close()

if __name__=="main":
    parser = argparse.ArgumentParser(description="Client CLI")
    parser.add_argument("name", help="Client Name", default="Nameless")
    args = parser.parse_args()
    client_name = args.name
    ping_server(SERVER_ID, client_name)
