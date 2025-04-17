import zmq
import sys

for i in range(3):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect("tcp://localhost:1111")

    print(f"Client {i+1} connected to server.")

    # Get name from command line arguments or use default
    message = f"Client {i+1} here."
    socket.send_string(message)

    # Get the reply
    print(" Waiting for reply...")
    response = socket.recv_string()
    print(f" Received: {response}") 

    context.destroy()
    socket.close()