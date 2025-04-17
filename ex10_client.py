import Pyro4
import sys
import random

def display_menu():
    """Display the operation menu"""
    print("\nStatistics Operations:")
    print("1. Calculate Mean")
    print("2. Calculate Median")
    print("3. Exit")
    return input("Enter your choice (1-3): ")

def get_numbers():
    try:
        nums_str = input("Enter numbers separated by spaces: ")
        return [float(x) for x in nums_str.split()]
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return None


def main():
    # Get the load balancer URI
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        uri = input("Enter the load balancer URI: ")
    
    load_balancer = Pyro4.Proxy(uri)
    
    while True:
        try:
            choice = display_menu()
            
            if choice == '1':  # Mean
                numbers = get_numbers()
                if numbers:
                    print(f"Numbers: {numbers}")
                    result = load_balancer.calculate_mean(numbers)
                    
                    print(f"\nMean: {result['result']}")
                    print(f"Computation time: {result['computation_time']:.6f} seconds")
                    print(f"Total request time: {result['load_balancer_time']:.6f} seconds")
                    print(f"From cache: {result['cached']}")
                    print(f"Handled by server: {result['server_id']}")
                    
            elif choice == '2':  # Median
                numbers = get_numbers()
                if numbers:
                    print(f"Numbers: {numbers}")
                    result = load_balancer.calculate_median(numbers)
                    
                    print(f"\nMedian: {result['result']}")
                    print(f"Computation time: {result['computation_time']:.6f} seconds")
                    print(f"Total request time: {result['load_balancer_time']:.6f} seconds")
                    print(f"From cache: {result['cached']}")
                    print(f"Handled by server: {result['server_id']}")
                    
            elif choice == '3':  # Exit
                break
                
            else:
                print("Invalid choice. Please select a number between 1 and 3.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("Client shutting down...")

if __name__ == "__main__":
    main() 