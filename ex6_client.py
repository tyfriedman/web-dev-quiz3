import Pyro4
import sys

def main():
    # Get the server URI from command line or use the default
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        uri = input("Enter the server URI: ")
    
    # Connect to the server
    server = Pyro4.Proxy(uri)
    
    greeting_count = 0
    
    while True:
        try:
            # Get name input from the user
            name = input("Enter your name (or 'exit' to quit): ")
            
            if name.lower() == 'exit':
                break
                
            # Call the greet method
            greeting = server.greet(name)
            print(greeting)
            
            greeting_count += 1
            
            # After every 3 greetings, display the history
            if greeting_count % 3 == 0:
                history = server.get_history()
                print("\nGreeting history:")
                for i, name in enumerate(history, 1):
                    print(f"{i}. {name}")
                print()
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    print("Client shutting down...")

if __name__ == "__main__":
    main() 