import Pyro4
import time

@Pyro4.expose
class LoadBalancer:
    def __init__(self, server_uris):
        self.server_uris = server_uris
        self.servers = [Pyro4.Proxy(uri) for uri in server_uris]
        self.current_server_index = 0
        
    def _get_next_server(self):
        """Get next server in round-robin fashion"""
        server = self.servers[self.current_server_index]
        # Update index for next request
        self.current_server_index = (self.current_server_index + 1) % len(self.servers)
        return server
        
    def calculate_mean(self, numbers):
        """Forward mean calculation to the next server"""
        server = self._get_next_server()
        start_time = time.time()
        
        try:
            result = server.calculate_mean(numbers)
            # Add load balancer timing info
            total_time = time.time() - start_time
            result['load_balancer_time'] = total_time
            
            return result
        except Exception as e:
            print(f"Error forwarding mean calculation to server: {e}")
            # Try the other server if one fails
            self.current_server_index = (self.current_server_index + 1) % len(self.servers)
            return self.calculate_mean(numbers)
            
    def calculate_median(self, numbers):
        """Forward median calculation to the next server"""
        server = self._get_next_server()
        start_time = time.time()
        
        try:
            result = server.calculate_median(numbers)
            # Add load balancer timing info
            total_time = time.time() - start_time
            result['load_balancer_time'] = total_time
            
            return result
        except Exception as e:
            print(f"Error forwarding median calculation to server: {e}")
            # Try the other server if one fails
            self.current_server_index = (self.current_server_index + 1) % len(self.servers)
            return self.calculate_median(numbers)

def main():
    # Define the URIs for the two stats servers
    stats_server1_uri = input("Enter URI for stats server 1: ")
    stats_server2_uri = input("Enter URI for stats server 2: ")
    
    server_uris = [stats_server1_uri, stats_server2_uri]
    
    # Create and register the load balancer
    balancer = LoadBalancer(server_uris)
    daemon = Pyro4.Daemon()
    uri = daemon.register(balancer)
    
    print(f"Load balancer started. Object URI: {uri}")
    print(f"Managing servers: {', '.join(server_uris)}")
    
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("Load balancer shutting down...")

if __name__ == "__main__":
    main() 