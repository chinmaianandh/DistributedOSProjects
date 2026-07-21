import socket
import argparse
import time, random, math
from common_utils import log_time
import grpc
import messages_pb2, messages_pb2_grpc

SERVER_ID = "0.0.0.0:50051"

stock_options = ["GameStart", "RottenFishCo", "BoarCo", "MenhirCo"]


def ping_server(channel, client_name):
        stub = messages_pb2_grpc.StockMessageStub(channel)

        stock_name = random.choice(stock_options)
        update_price = random.random()*100
        print(f"\n{client_name}\t[{log_time()}]\tSending Lookup {stock_name}")
        reply = stub.Update(messages_pb2.UpdateRequest(stock_name=stock_name, price=update_price))
        print(f"{client_name}\t[{log_time()}]\tReceived : {reply}")

def ping_n_times(SERVER_ID, client_name, num_reqs):
    with grpc.insecure_channel(SERVER_ID) as channel:
        for i in range(num_reqs):
            ping_server(channel, client_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client CLI")
    parser.add_argument("--name", help="Client Name", default="Nameless")
    parser.add_argument("--num_reqs", type=int, help="Num. of Requests to send", default=10)
    args = parser.parse_args()
    client_name = args.name
    num_reqs = args.num_reqs
    ping_n_times(SERVER_ID, client_name, num_reqs)
