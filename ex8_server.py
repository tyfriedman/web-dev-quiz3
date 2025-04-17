import Pyro4
import datetime
import threading

@Pyro4.expose
class ListProcessingServer:
    def __init__(self):
        self.log_file = "server_log.txt"
        self.last_caller = None
        self.lock = threading.Lock()
    
    def _log_operation(self, client_id, method_name):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Client: {client_id} | Method: {method_name}\n"
        
        with self.lock:
            # Set the last caller
            self.last_caller = client_id
            
            # Write to log file
            with open(self.log_file, "a") as f:
                f.write(log_entry)
    
    def reverse_list(self, client_id, lst):
        self._log_operation(client_id, "reverse_list")
        return list(reversed(lst))
    
    def remove_duplicates(self, client_id, lst):
        self._log_operation(client_id, "remove_duplicates")
        return list(dict.fromkeys(lst))
    
    def get_last_caller(self):
        with self.lock:
            return self.last_caller

def main():
    server = ListProcessingServer()
    daemon = Pyro4.Daemon()
    uri = daemon.register(server)
    
    print(f"Server URI: {uri}")
    print("List Processing Server is running.")
    
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    main() 