import socket
import argparse
import time, random, math
from common_utils import log_time
import grpc
import messages_pb2, messages_pb2_grpc

SERVER_ID = "0.0.0.0:50051"

stock_options = ["GameStart", "RottenFishCo", "BoarCo", "MenhirCo"]



def ping_server_trade(channel, client_name):     
    trade_options = [messages_pb2.TradeAction.TRADE_SELL, messages_pb2.TradeAction.TRADE_BUY]
    stub = messages_pb2_grpc.StockMessageStub(channel)

    stock_name = random.choice(stock_options)
    print(f"\n{client_name}\t[{log_time()}]\tSending TradeReq {stock_name}")
    reply = stub.Trade(messages_pb2.TradeRequest(stock_name=stock_name, num_of_items=random.randint(50, 100), trade_type=random.choice(trade_options)))
    print(f"{client_name}\t[{log_time()}]\tReceived TradeResp : {reply}")


def ping_server_lookup(channel, client_name):
    stub = messages_pb2_grpc.StockMessageStub(channel)

    stock_name = random.choice(stock_options)
    print(f"\n{client_name}\t[{log_time()}]\tSending LookupReq {stock_name}")
    reply = stub.Lookup(messages_pb2.LookupRequest(stock_name=stock_name))
    print(f"{client_name}\t[{log_time()}]\tReceived LookupResp : {reply}")

def ping_server(channel, client_name):
    ping_options = ["Lookup", "Trade"]
    action = random.choice(ping_options)
    if action=='Lookup':
        ping_server_lookup(channel, client_name)
    elif action=='Trade':
        ping_server_trade(channel, client_name)


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
