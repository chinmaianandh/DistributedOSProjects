import socket, argparse
import time, random, json
import threading
from common_utils import log_time

SERVER_ID = ("0.0.0.0", 8888)

stocks = {
    "GameStart" : {"price" : 120.5, "volume" : 0},
    "RottenFishCo" : {"price" : 52.3, "volume" : 0},
}

parser = argparse.ArgumentParser(description="Server CLI")
parser.add_argument("thread_count", type=int, help="no. of threads in threadPool", default=5)
args = parser.parse_args()

max_thread_cnt = args.thread_count
queue_lock = threading.Condition()
request_queue = []

def process_request(req_msg):
    parts = req_msg.strip().split()
    if(len(parts)!=2 or parts[0]!='Lookup'):
        return {"error" : f"Invalid Msg : '{req_msg}'"}
    resp_json = {}
    if parts[1] not in stocks:
        resp_json["status"] = -1
    else:
        resp_json["status"] = 1
        resp_json["price"] = stocks[parts[1]]["price"]
    return json.dumps(resp_json)

def start_worker():
    while(True):
        conn = False
        with queue_lock:
            while not request_queue:
                queue_lock.wait()
            conn, client_addr = request_queue.pop(0)
        with conn:
            try:
                data = conn.recv(1024)
                print(f"[{log_time()}]\tGot MSG : {data.decode()}")
                resp = process_request(data.decode())
                time.sleep(5+random.random())
                print(f"[{log_time()}]\tSending Resp : {resp}")
                conn.sendall(resp.encode())
            except Exception as e:
                print(f"[{log_time()}]\tException - {e}")
        
def start_pool(n):
    for _ in range(n):
        threading.Thread(target=start_worker, daemon=True).start()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(SERVER_ID)

s.listen(5)

start_pool(max_thread_cnt)

while(1):
    conn, client_addr = s.accept()
    with queue_lock:
        request_queue.append((conn, client_addr))
        queue_lock.notify()
    