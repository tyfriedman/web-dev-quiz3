import Pyro4

@Pyro4.expose
class GreetingServer:
    def __init__(self):
        self.greet_history = []
    
    def greet(self, name):
        """Greets a person and stores their name in history"""
        self.greet_history.append(name)
        return f"Hello, {name}!"
    
    def get_history(self):
        """Returns the list of all names greeted so far"""
        return self.greet_history

def main():
    # Start the Pyro4 server
    server = GreetingServer()
    daemon = Pyro4.Daemon()
    uri = daemon.register(server)
    
    print(f"Server URI: {uri}")
    print("Server is running.")
    
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    main() 