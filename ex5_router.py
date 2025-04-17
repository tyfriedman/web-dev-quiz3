import zmq
import time

context = zmq.Context()
server = context.socket(zmq.ROUTER)
server.bind("tcp://*:5555")

print("Chat server started on port 5555")

# Keep track of connected clients
clients = {}

try:
    while True:
        # Wait for a message
        identity, message = server.recv_multipart()
        
        # Decode message from bytes to string
        message_str = message.decode('utf-8')
        
        # Handle client messages
        if message_str.startswith("CONNECT:"):
            username = message_str[8:]  # Extract username after "CONNECT:"
            clients[identity] = username
            print(f"{username} has joined the chat")
            
            # Broadcast join notification to other clients
            join_notification = f"SERVER: {username} has joined the chat"
            for client_id in clients:
                if client_id != identity:  # Don't send to the client who just connected
                    server.send_multipart([client_id, join_notification.encode('utf-8')])
        
        elif message_str == "exit":
            # Client is disconnecting
            if identity in clients:
                username = clients[identity]
                print(f"{username} has left the chat")
                
                # Remove client from the list
                del clients[identity]
                
                # Broadcast leave notification to remaining clients
                leave_notification = f"SERVER: {username} has left the chat"
                for client_id in clients:
                    server.send_multipart([client_id, leave_notification.encode('utf-8')])
        
        else:
            # Regular chat message - broadcast to all other clients
            if identity in clients:
                sender = clients[identity]
                print(f"Message from {sender}: {message_str}")
                
                # Broadcast to all other clients
                for client_id in clients:
                    if client_id != identity:  # Don't send back to the sender
                        server.send_multipart([client_id, f"{sender}: {message_str}".encode('utf-8')])
                        
except KeyboardInterrupt:
    print("Server shutting down...")
    server.close()
    context.term() 