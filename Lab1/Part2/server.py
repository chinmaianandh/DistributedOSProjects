import socket, argparse
import time, random, json
import threading
from common_utils import log_time
import grpc
import messages_pb2, messages_pb2_grpc
from concurrent import futures
from google.protobuf.json_format import MessageToDict

SERVER_ID = "0.0.0.0:50051"

class StockServicer(messages_pb2_grpc.StockMessageServicer):
    def __init__(self, max_volume):
        self.stocks = {
            "GameStart" : {"price" : 120.5, "volume" : 1},
            "RottenFishCo" : {"price" : 52.3, "volume" : 2},
            "BoarCo" : {"price" : 25.87, "volume" : 3},
            "MenhirCo" : {"price" : 20.6, "volume" : 4},
        }
        print("Initializing Stock Service!!")
        for _, s in self.stocks.items():
            s['lock'] = threading.Lock()
            s['max_volume'] = max_volume


    def GetStock(self, stock_name):
        if stock_name in self.stocks:
            return self.stocks[stock_name]
        return False

    def Lookup(self, request, context):
        print(f"\n[{log_time()}]\tGot LookupReq : {MessageToDict(request, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
        # time.sleep(2+random.random())
        got = self.GetStock(request.stock_name)

        reply = messages_pb2.LookupResponse(status_code=-1, price=0, volume=0)
        if(got!=False):
            reply.status_code = 0
            with got['lock']:
                reply.price = got['price']
                reply.volume = got['volume']
        print(f"[{log_time()}]\tSending LookupResp : {MessageToDict(reply, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
        return reply
    
    def Trade(self, request, context):
        print(f"\n[{log_time()}]\tGot TradeReq : {MessageToDict(request, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
        # time.sleep(2+random.random())
        reply = messages_pb2.TradeResponse(status_code=-1)
        if request.stock_name in self.stocks:
            with self.stocks[request.stock_name]['lock']:
                if self.stocks[request.stock_name]['volume']+request.num_of_items > self.stocks[request.stock_name]['max_volume']:
                    reply.status_code = 0
                else:
                    self.stocks[request.stock_name]['volume'] += request.num_of_items
                    reply.status_code = 1
        print(f"[{log_time()}]\tSending TradeResp : {MessageToDict(reply, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
        return reply

    def Update(self, request, context):
        print(f"\n[{log_time()}]\tGot UpdateReq : {MessageToDict(request, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
        # time.sleep(2+random.random())
        reply = messages_pb2.UpdateResponse(status_code=-2)
        if request.price>=0:
            if request.stock_name not in self.stocks:
                reply.status_code = -1
            else:
                with self.stocks[request.stock_name]['lock']:
                    self.stocks[request.stock_name]['price'] = request.price
                    reply.status_code = 1
        print(f"[{log_time()}]\tSending UpdateResp : {MessageToDict(reply, always_print_fields_with_no_presence=True, preserving_proto_field_name=True)}")
        return reply


def serve(max_workers = 5, max_volume=100):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        maximum_concurrent_rpcs=20,
    )
    messages_pb2_grpc.add_StockMessageServicer_to_server(StockServicer(max_volume), server)
    server.add_insecure_port(SERVER_ID)
    server.start()
    print(f"serving on {SERVER_ID}")
    server.wait_for_termination()

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Server CLI")
    parser.add_argument("--thread_count", type=int, help="no. of threads in threadPool", default=2)
    parser.add_argument("--max_volume", type=int, help="Max trading volume allowed per stock.", default=100)
    args = parser.parse_args()
    max_thread_cnt = args.thread_count
    max_volume = args.max_volume

    serve(max_thread_cnt, max_volume)
