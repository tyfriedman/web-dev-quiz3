import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

topics = ["sports", "weather", "tech", "politics"]
news_by_topic = {
    "sports":   "Game finished. Notre Dame won 3-1",
    "weather":  "Sunny skies expected for the weekend",
    "tech":     "Major software update released",
    "politics": "Election results announced"
}

print("Publisher started. Broadcasting news...")

while True:
    topic = random.choice(topics)
    message = f"{topic}: Breaking news - {news_by_topic[topic]}"
    
    print(f"{message}")
    socket.send_string(message)
    
    time.sleep(2)
