import zmq
import time
import datetime

# Setup ZMQ context
context = zmq.Context()

# Create PULL socket to receive tasks from ventilator
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

worker_id = "Worker 2"
print(f"{worker_id} started and waiting for tasks...")

# Process tasks until receiving DONE message
while True:
    message = receiver.recv_string()
    
    # Check if it's the termination signal
    if message == "DONE":
        print(f"{worker_id} received DONE signal, shutting down")
        break
        
    # Get timestamp when task was received
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    # Parse the task message
    task_id = message
    
    # Simulate actual work
    print(f"{worker_id} received task {task_id} at {timestamp}. Processing task {task_id}...")
    time.sleep(0.1)  # Convert workload to seconds

print(f"{worker_id} finished all tasks and is shutting down") 