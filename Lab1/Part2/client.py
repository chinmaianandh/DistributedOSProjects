import socket
import argparse
import time, random, math
from common_utils import log_time, timer
import grpc
import messages_pb2, messages_pb2_grpc
from google.protobuf.json_format import MessageToDict

stock_options = ["GameStart", "RottenFishCo", "BoarCo", "MenhirCo"]



def ping_server_trade(channel, client_name):     
    trade_options = [messages_pb2.TradeAction.TRADE_SELL, messages_pb2.TradeAction.TRADE_BUY]
    stub = messages_pb2_grpc.StockMessageStub(channel)

    stock_name = random.choice(stock_options)
    request = messages_pb2.TradeRequest(stock_name=stock_name, num_of_items=random.randint(50, 100), trade_type=random.choice(trade_options))
    print(f"\n{client_name}\t[{log_time()}]\tSending TradeReq {MessageToDict(request, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
    with timer(client_name, "trade"):
        reply = stub.Trade(request)
    print(f"{client_name}\t[{log_time()}]\tReceived TradeResp : {MessageToDict(reply, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")


def ping_server_lookup(channel, client_name):
    stub = messages_pb2_grpc.StockMessageStub(channel)

    stock_name = random.choice(stock_options)
    request = messages_pb2.LookupRequest(stock_name=stock_name)
    print(f"\n{client_name}\t[{log_time()}]\tSending LookupReq {MessageToDict(request, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
    with timer(client_name, "lookup"):
        reply = stub.Lookup(request)
    print(f"{client_name}\t[{log_time()}]\tReceived LookupResp : {MessageToDict(reply, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")

def ping_server_update(channel, client_name):
    stub = messages_pb2_grpc.StockMessageStub(channel)

    stock_name = random.choice(stock_options)
    update_price = random.random()*100
    request = messages_pb2.UpdateRequest(stock_name=stock_name, price=update_price)
    print(f"\n{client_name}\t[{log_time()}]\tSending UpdateReq {MessageToDict(request, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
    with timer(client_name, "update"):
        reply = stub.Update(request)
    print(f"{client_name}\t[{log_time()}]\tReceived UpdateResp : {MessageToDict(reply, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")

method_dict = {
    'lookup' : ping_server_lookup,
    'trade' : ping_server_trade,
    'update' : ping_server_update,
}

def ping_server(channel, client_name, method_name):
    if(method_name=='random'):
        ping_options = list(method_dict.values())
        action = random.choice(ping_options)
        action(channel, client_name)
    else:
        method_dict[method_name](channel, client_name)
        
def ping_n_times(SERVER_ID, client_name, num_reqs, method_name):
    with grpc.insecure_channel(SERVER_ID) as channel:
        for i in range(num_reqs):
            ping_server(channel, client_name, method_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client CLI")
    parser.add_argument("--name", help="Client Name", default="Nameless")
    parser.add_argument("--num_reqs", type=int, help="Num. of Requests to send", default=10)
    parser.add_argument("--mode", help="Which gRPC method to ping? options = ('lookup', 'trade', 'update', 'random')", choices=["lookup", "trade", "update", "random"], default="random")
    parser.add_argument("--server", help="Server address and port - default = 'localhost:50051'", default="localhost:50051")
    args = parser.parse_args()
    client_name = args.name
    num_reqs = args.num_reqs
    method_name = args.mode
    SERVER_ID = args.server
    ping_n_times(SERVER_ID, client_name, num_reqs, method_name)
