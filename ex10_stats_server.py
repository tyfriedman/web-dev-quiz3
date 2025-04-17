import Pyro4
import statistics
import time
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        
    def get(self, key):
        if key not in self.cache:
            return None  # not in cache
        # Move key to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
        
    def put(self, key, value):
        self.cache[key] = value
        # Move to end or add at the end
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            # Remove least recently used item
            self.cache.popitem(last=False)
            
    def show(self):
        print("Current cache state:")
        for k, v in self.cache.items():
            print(f"{k} => {v}")

@Pyro4.expose
class StatsServer:
    def __init__(self, server_id):
        self.server_id = server_id
        self.cache = LRUCache(capacity=3)  # Store last 3 unique calculations
        
    def calculate_mean(self, numbers):
        start_time = time.time()
        
        # Convert list to tuple for hashing as dictionary key
        key = tuple(numbers)
        
        # Check if result is in cache
        cached_result = self.cache.get(key)
        if cached_result and cached_result[0] == 'mean':
            computation_time = time.time() - start_time
            print(f"Server {self.server_id}: Cache hit for mean calculation")
            return {
                'result': cached_result[1], 
                'computation_time': computation_time,
                'cached': True,
                'server_id': self.server_id
            }
        
        # Calculate mean and measure time
        result = statistics.mean(numbers)
        
        # Store in cache
        self.cache.put(key, ('mean', result))
        
        computation_time = time.time() - start_time
        print(f"Server {self.server_id}: Calculated mean: {result}, time: {computation_time:.6f}s")
        
        return {
            'result': result, 
            'computation_time': computation_time,
            'cached': False,
            'server_id': self.server_id
        }
        
    def calculate_median(self, numbers):
        start_time = time.time()
        
        # Convert list to tuple for hashing as dictionary key
        key = tuple(numbers)
        
        # Check if result is in cache
        cached_result = self.cache.get(key)
        if cached_result and cached_result[0] == 'median':
            computation_time = time.time() - start_time
            print(f"Server {self.server_id}: Cache hit for median calculation")
            return {
                'result': cached_result[1], 
                'computation_time': computation_time,
                'cached': True,
                'server_id': self.server_id
            }
        
        # Calculate median and measure time
        result = statistics.median(numbers)
        
        # Store in cache
        self.cache.put(key, ('median', result))
        
        computation_time = time.time() - start_time
        print(f"Server {self.server_id}: Calculated median: {result}, time: {computation_time:.6f}s")
        
        return {
            'result': result, 
            'computation_time': computation_time,
            'cached': False,
            'server_id': self.server_id
        }

def start_server(server_id, port):
    server = StatsServer(server_id)
    daemon = Pyro4.Daemon(port=port)
    uri = daemon.register(server, f"stats{server_id}")
    
    print(f"Stats Server {server_id} started. Object URI: {uri}")
    
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print(f"Stats Server {server_id} shutting down...")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python ex10_stats_server.py <server_id> <port>")
        print("Example: python ex10_stats_server.py 1 9091")
        sys.exit(1)
    
    server_id = int(sys.argv[1])
    port = int(sys.argv[2])
    
    start_server(server_id, port) 