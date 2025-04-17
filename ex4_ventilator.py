import zmq
import time
import sys

# Setup ZMQ context
context = zmq.Context()

# Create PUSH socket to send tasks to workers
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

print("Sending tasks to workers...")

# Send 10 tasks
for task_id in range(10):
    sender.send_string(f"{task_id}")
    print(f"Sent task {task_id}")
    time.sleep(0.1)  # Small delay between tasks

# Wait a bit before sending DONE signals
time.sleep(1)  

# Send DONE message to each worker (we'll send 2 since we have 2 workers)
for _ in range(2):
    sender.send_string("DONE")

print("All tasks sent, ventilator shutting down") 