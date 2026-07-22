import time, csv
import os, socket
from contextlib import contextmanager
from pathlib import Path




def log_time():
    return time.strftime("%H:%M:%S", time.localtime())

def log_row(client_name, method, elapsed):
    Path("/app/results/").mkdir(parents=True, exist_ok=True)   
    RESULTS = f"/app/results/{client_name}.csv"
    new = not os.path.exists(RESULTS)
    with open(RESULTS, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["client", "method", "latency(ms)"])
        w.writerow([client_name, method, elapsed])
        

@contextmanager
def timer(client_name, label):
    t0 = time.perf_counter()
    yield
    log_row(client_name, label, 1000*(time.perf_counter() - t0))