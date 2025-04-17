import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

print("All-topics subscriber started. Listening for all news...")

while True:
    message = socket.recv_string()
    print(f"Received: {message}")
