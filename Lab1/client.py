import socket
import argparse
import time, random, math
from common_utils import log_time

SERVER_ID = ("0.0.0.0", 8888)

stock_options = ["GameStart", "RottenFishCo"]

def ping_server(SERVER_ID, client_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ID)

    stock_name = random.choice(stock_options)
    print(f"{client_name}\t[{log_time()}]\tSending Lookup {stock_name}")
    s.sendall(f"Lookup {stock_name}".encode())

    data = s.recv(1024)

    print(f"{client_name}\t[{log_time()}]\tReveived : {data.decode()}")

    s.close()

def ping_n_times(SERVER_ID, client_name, num_reqs):
    for i in range(num_reqs):
        ping_server(SERVER_ID, client_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client CLI")
    parser.add_argument("--name", help="Client Name", default="Nameless")
    parser.add_argument("--num_reqs", type=int, help="Num. of Requests to send", default=10)
    args = parser.parse_args()
    client_name = args.name
    num_reqs = args.num_reqs
    ping_n_times(SERVER_ID, client_name, num_reqs)
