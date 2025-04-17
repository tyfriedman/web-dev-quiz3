import zmq
import datetime

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.setsockopt(zmq.LINGER, 0)
socket.bind("tcp://localhost:1111")

print("Server started, waiting for connection...")

# Wait for next request from client
name = socket.recv_string()

# connected - print time and send greeting
print(f"Client connected. Time is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
response = f"Hello, {name}!"

# Send reply back to client
socket.send_string(response) 