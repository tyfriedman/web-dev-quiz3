import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.LINGER, 0)
socket.connect("tcp://localhost:1111")

print("Client connected to server.")

# Get name from command line arguments or use default
if len(sys.argv) > 1:
    name = sys.argv[1]
    message = f"{name}"
else:
    message = "anonymous"

print(f"Sending: {message}")
socket.send_string(message)

# Get the reply
response = socket.recv_string()
print(f"Received: {response}") 

context.destroy()
socket.close()