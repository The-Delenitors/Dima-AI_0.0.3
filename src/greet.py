import numpy as np
from text_to_speech import speak

def greet():
        # Getting a random number and using that to determine which preset greets to use
        a = np.random.choice([0, 1, 2])
        
        if a == 0:
            greeting = "Hello, how can I assist you today?"
        elif a == 1:
            greeting = "Hi, What can I do for you?"
        else:
            greeting = "Dima A I here!"

        speak(greeting)