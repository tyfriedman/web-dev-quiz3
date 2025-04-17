import Pyro4
import re
from collections import Counter

@Pyro4.expose
class TextAnalysisServer:
    def __init__(self):
        pass
    
    def _tokenize(self, text):
        """Convert text to lowercase and split into words, removing punctuation"""
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def word_count(self, text):
        words = self._tokenize(text)
        return len(words)
    
    def most_common_word(self, text):
        words = self._tokenize(text)
        if not words:
            return None
            
        word_counts = Counter(words)
        most_common = word_counts.most_common(1)
        return most_common[0]  # Returns (word, count) tuple
    
    def contains_word(self, text, word):
        words = self._tokenize(text)
        return word.lower() in words

def main():
    server = TextAnalysisServer()
    daemon = Pyro4.Daemon()
    uri = daemon.register(server)
    
    print(f"Server URI: {uri}")
    print("Text Analysis Server is running.")
    
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    main() 