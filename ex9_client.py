import Pyro4
import sys
import os.path

def display_menu():
    """Display the operation menu"""
    print("\nText Analysis Options:")
    print("1. Count words in text")
    print("2. Find most common word in text")
    print("3. Check if text contains a specific word")
    print("4. Change text")
    print("5. Exit")
    return input("Enter your choice (1-5): ")

def get_text():
    """Get text from user input or a file"""
    input_choice = input("Enter text (1) manually or (2) from a file? (1/2): ")
    
    if input_choice == '1':
        return input("Enter your text: ")
    elif input_choice == '2':
        file_path = input("Enter the file path: ")
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    return file.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return None
        else:
            print(f"File not found: {file_path}")
            return None
    else:
        print("Invalid choice")
        return None

def main():
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        uri = input("Enter the server URI: ")
    
    server = Pyro4.Proxy(uri)
    
    # Get text once at the beginning
    print("Please enter the text to analyze:")
    text = get_text()
    if not text:
        print("No valid text provided. Exiting.")
        return
    
    print(f"\nAnalyzing text ({len(text)} characters, approximately {text.count(' ') + 1} words)")
    
    while True:
        try:
            choice = display_menu()
            
            if choice == '1':  # Word Count
                count = server.word_count(text)
                print(f"Word count: {count} words")
                    
            elif choice == '2':  # Most Common Word
                result = server.most_common_word(text)
                if result:
                    word, count = result
                    print(f"Most common word: '{word}' (appears {count} times)")
                else:
                    print("No words found in the text")
                    
            elif choice == '3':  # Contains Word
                word = input("Enter the word to search for: ")
                contains = server.contains_word(text, word)
                if contains:
                    print(f"The word '{word}' is present in the text")
                else:
                    print(f"The word '{word}' is NOT present in the text")
            
            elif choice == '4':  # Change text
                print("Please enter new text to analyze:")
                new_text = get_text()
                if new_text:
                    text = new_text
                    print(f"\nAnalyzing new text ({len(text)} characters, approximately {text.count(' ') + 1} words)")
                    
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