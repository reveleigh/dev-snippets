import _thread
import time

# Global shared variable
shared_value = 0

# Create a lock
lock = _thread.allocate_lock()

def update_value():
  global shared_value
  while True:
    # Acquire the lock before modifying the shared variable
    lock.acquire()
    shared_value += 1
    print(f"Updated value to: {shared_value}")
    # Release the lock
    lock.release()
    time.sleep(1)  # Introduce a delay to avoid rapid updates

def read_value():
  global shared_value
  while True:
    # Acquire the lock before reading the shared variable
    lock.acquire()
    print(f"Read value: {shared_value}")
    # Release the lock
    lock.release()
    time.sleep(0.5)  # Introduce a delay to avoid rapid reads

# Create and run threads
_thread.start_new_thread(update_value, ())  # This will run on core 0 by default

# Keep the main thread alive (you might need to interrupt this manually)
while True:
    read_value()
    time.sleep(0.5)
