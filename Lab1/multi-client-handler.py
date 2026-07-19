import threading, time, random
from client import ping_server

SERVER_ID = ("0.0.0.0", 8888)

# ts = [threading.Thread(target=ping_server, args=(SERVER_ID, f"client_T_{i}"), daemon=True) for i in range(10)]

for i in range(10):
    t = threading.Thread(target=ping_server, args=(SERVER_ID, "client_T_"+str(i)), daemon=False)
    t.start()
    time.sleep(random.random()/2)
