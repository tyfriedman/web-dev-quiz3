import zmq
import sys
import threading
import time

context = zmq.Context()
client = context.socket(zmq.DEALER)
client.connect("tcp://localhost:5555")

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = input("Enter your username: ")

# Send connect message with username
client.send(f"CONNECT:{username}".encode('utf-8'))

def receive_messages():
    """Thread function to receive and display messages"""
    while True:
        try:
            message = client.recv().decode('utf-8')
            print(f"\n{message}")
            print("> ", end="", flush=True)  # Re-print the prompt
        except zmq.ZMQError:
            # Socket has been closed
            break
        except KeyboardInterrupt:
            break

# Start the receive thread
receiver_thread = threading.Thread(target=receive_messages, daemon=True)
receiver_thread.start()

print(f"Connected to chat server as {username}")
print("Type 'exit' to leave the chat")

try:
    while True:
        message = input("> ")
        if message.lower() == "exit":
            client.send("exit".encode('utf-8'))
            break
        else:
            client.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("\nDisconnecting...")

# Clean up
time.sleep(0.1)
client.close()
context.term()
print("Disconnected from server") 