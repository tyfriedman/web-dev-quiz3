import zmq
import sys

topic = "sports"  # Subscribe only to sports news

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, topic)

print(f"Subscriber started. Listening for {topic} news...")

while True:
    message = socket.recv_string()
    print(f"Received: {message}")