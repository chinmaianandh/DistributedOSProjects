import socket, argparse
import time, random, json
import threading
from common_utils import log_time
import grpc
import messages_pb2, messages_pb2_grpc
from concurrent import futures

SERVER_ID = "localhost:50051"

class StockServicer(messages_pb2_grpc.StockMessageServicer):
    def __init__(self):
        self.stocks = {
            "GameStart" : {"price" : 120.5, "volume" : 1},
            "RottenFishCo" : {"price" : 52.3, "volume" : 2},
            "BoarCo" : {"price" : 25.87, "volume" : 3},
            "MenhirCo" : {"price" : 20.6, "volume" : 4},
        }
        self.stock_lock = threading.Lock()

    def GetStock(self, stock_name):
        with self.stock_lock:
            if stock_name in self.stocks:
                return self.stocks[stock_name]
        return False

    def Lookup(self, request, context):
        print(f"\n[{log_time()}]\tGot MSG : {request}")
        time.sleep(5+random.random())
        got = self.GetStock(request.stock_name)

        reply = messages_pb2.LookupResponse(status_code=-1, price=0, volume=0)
        if(got):
            reply.status_code = 0
            reply.price = got['price']
            reply.volume = got['volume']
        print(f"[{log_time()}]\tSending Resp : {reply}")
        return reply


def serve(max_workers = 5):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers),
        maximum_concurrent_rpcs=20,
    )
    messages_pb2_grpc.add_StockMessageServicer_to_server(StockServicer(), server)
    server.add_insecure_port(SERVER_ID)
    server.start()
    print(f"serving on {SERVER_ID}")
    server.wait_for_termination()

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Server CLI")
    parser.add_argument("--thread_count", type=int, help="no. of threads in threadPool", default=5)
    args = parser.parse_args()
    max_thread_cnt = args.thread_count

    serve(max_thread_cnt)
