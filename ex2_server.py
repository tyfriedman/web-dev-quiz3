import zmq
import random, time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.setsockopt(zmq.LINGER, 0)
socket.bind("tcp://localhost:1111")

print("Server started, waiting for connection...")

client_id = 0
while True:
    # Wait for next request from client
    client_message = socket.recv_string()
    client_id += 1

    # connected - print client identifier and message
    print(f"Client {client_id} connected.")
    print(f" Message received: {client_message}")

    # Send reply back to client
    time.sleep(random.randint(1, 5))
    response = f"Received from Client {client_id}"
    socket.send_string(response) 