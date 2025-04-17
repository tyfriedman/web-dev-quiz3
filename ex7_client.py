import Pyro4
import sys

def display_menu():
    """Display the operation menu"""
    print("\nAvailable operations:")
    print("1. Add")
    print("2. Subtract")
    print("3. Divide")
    print("4. View operation counts")
    print("5. Exit")
    return input("Enter your choice (1-5): ")

def get_numbers():
    """Get two numbers from the user"""
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        return a, b
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return None, None

def main():
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
            
            if choice == '1':  # Add
                a, b = get_numbers()
                if a is not None and b is not None:
                    result = server.add(a, b)
                    print(f"Result: {a} + {b} = {result}")
                    
            elif choice == '2':  # Subtract
                a, b = get_numbers()
                if a is not None and b is not None:
                    result = server.subtract(a, b)
                    print(f"Result: {a} - {b} = {result}")
                    
            elif choice == '3':  # Divide
                a, b = get_numbers()
                if a is not None and b is not None:
                    try:
                        result = server.divide(a, b)
                        print(f"Result: {a} / {b} = {result}")
                    except Exception as e:
                        print(f"Error: {str(e)}")
                        
            elif choice == '4':  # View operation counts
                counts = server.operation_count()
                print("\nOperation Counts:")
                for op, count in counts.items():
                    print(f"{op.capitalize()}: {count}")
                    
            elif choice == '5':  # Exit
                break
                
            else:
                print("Invalid choice. Please select a number between 1 and 5.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("Client shutting down...")

if __name__ == "__main__":
    main() 