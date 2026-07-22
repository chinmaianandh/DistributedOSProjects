import threading, time, random
from client import ping_n_times

SERVER_ID = "localhost:50051"

ts = []
for i in range(10):
    t = threading.Thread(target=ping_n_times, args=(SERVER_ID, "client_T_"+str(i), 10), daemon=True)
    ts.append(t)
    t.start()
for t in ts:
    t.join()
