import socket, argparse
import time, random
import threading
from common_utils import log_time

SERVER_ID = ("0.0.0.0", 8888)

stocks = {
    "GameStart" : 120.5,
    "RottenFishCo" : 50.6,
}

parser = argparse.ArgumentParser(description="Server CLI")
parser.add_argument("thread_count", type=int, help="no. of threads in threadPool", default=5)
args = parser.parse_args()

max_thread_cnt = args.thread_count
queue_lock = threading.Condition()
request_queue = []

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
                print(f"{log_time()}\tGot MSG : {data.decode()}")
                time.sleep(10+random.random())
                print(f"{log_time()}\tSending Hello Back!!")
                conn.sendall(b"Hello back from Server")
            except Exception as e:
                print(f"{log_time()}\tException - {e}")
        
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
    