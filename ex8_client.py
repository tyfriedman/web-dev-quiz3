import Pyro4
import sys
import uuid
import ast

def generate_client_id():
    """Generate a unique client ID"""
    return str(uuid.uuid4())[:8]  # Using first 8 chars of UUID for readability

def display_menu():
    """Display the operation menu"""
    print("\nAvailable operations:")
    print("1. Reverse a list")
    print("2. Remove duplicates from a list")
    print("3. Check last caller")
    print("4. Exit")
    return input("Enter your choice (1-4): ")

def get_list():
    try:
        list_str = input("Enter a list (e.g., [1, 2, 3, 'a', 'b']): ")
        return ast.literal_eval(list_str)  # Safely evaluate the string as a Python expression
    except (SyntaxError, ValueError) as e:
        print(f"Invalid list format: {e}")
        return None

def main():
    # Generate a unique client ID
    client_id = generate_client_id()
    print(f"Your client ID is: {client_id}")
    
    # Get the server URI from command line or use the default
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        uri = input("Enter the server URI: ")
    
    # Connect to the server
    server = Pyro4.Proxy(uri)
    
    while True:
        try:
            choice = display_menu()
            
            if choice == '1':  # Reverse list
                lst = get_list()
                if lst is not None:
                    result = server.reverse_list(client_id, lst)
                    print(f"Original list: {lst}")
                    print(f"Reversed list: {result}")
                    
            elif choice == '2':  # Remove duplicates
                lst = get_list()
                if lst is not None:
                    result = server.remove_duplicates(client_id, lst)
                    print(f"Original list: {lst}")
                    print(f"List without duplicates: {result}")
                    
            elif choice == '3':  # Check last caller
                last_caller = server.get_last_caller()
                if last_caller:
                    print(f"Last client to call the server: {last_caller}")
                else:
                    print("No client has called the server yet.")
                    
            elif choice == '4':  # Exit
                break
                
            else:
                print("Invalid choice. Please select a number between 1 and 4.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("Client shutting down...")

if __name__ == "__main__":
    main() 