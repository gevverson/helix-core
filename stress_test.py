import threading
import requests
import time

# The Target: Your Dockerized Enterprise Server
URL = "http://127.0.0.1:8000/docs"
TOTAL_REQUESTS = 100

def attack_server(request_id):
    try:
        start = time.time()
        response = requests.get(URL)
        end = time.time()
        
        if response.status_code == 200:
            print(f"✅ Request {request_id}: Success in {round(end-start, 2)}s")
        else:
            print(f"❌ Request {request_id}: Failed (Status {response.status_code})")
    except Exception as e:
        print(f"🔥 Request {request_id}: CRASHED ({e})")

print(f"🚀 LAUNCHING {TOTAL_REQUESTS} REQUESTS AT HELIX CORE...")
threads = []

# Launch all 100 requests INSTANTLY
for i in range(TOTAL_REQUESTS):
    t = threading.Thread(target=attack_server, args=(i,))
    threads.append(t)
    t.start()

# Wait for all to finish
for t in threads:
    t.join()

print("\n🏁 TEST COMPLETE.")
