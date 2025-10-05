import threading
import time

def worker(name):
    print(f"Thread {name} starting")
    time.sleep(2)
    print(f"Thread {name} finished")

# Create threads
t1 = threading.Thread(target=worker, args=["A"])
t2 = threading.Thread(target=worker, args=["B"])

# Start threads
t1.start()
t2.start()

# Wait for threads to complete
t1.join()
t2.join()

print("All threads done!")


# Thread A starting
# Thread B starting
# Thread A finished
# Thread B finished
# All threads done!
