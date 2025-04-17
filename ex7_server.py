import Pyro4

class DivisionByZeroError(Exception):
    """Custom exception for division by zero"""
    pass

@Pyro4.expose
class ArithmeticServer:
    def __init__(self):
        self.operation_counts = {
            "add": 0,
            "subtract": 0,
            "divide": 0
        }
    
    def add(self, a, b):
        self.operation_counts["add"] += 1
        return a + b
    
    def subtract(self, a, b):
        self.operation_counts["subtract"] += 1
        return a - b
    
    def divide(self, a, b):
        if b == 0:
            raise DivisionByZeroError("Division by zero is not allowed")
        self.operation_counts["divide"] += 1
        return a / b
    
    def operation_count(self):
        return self.operation_counts

def main():
    server = ArithmeticServer()
    daemon = Pyro4.Daemon()
    uri = daemon.register(server)
    
    print(f"Server URI: {uri}")
    print("Arithmetic Server is running.")
    
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    main() 