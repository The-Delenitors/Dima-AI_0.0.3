# Hiding pygame's hello message
# import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from gtts import gTTS
import pygame
import io

# Initialize pygame mixer
pygame.mixer.init()

# Function to convert text to speech
def speak(text, language='en'):
    tts = gTTS(text=text, lang=language)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Example usage
# speak("Hello, I am speaking with Google's voice.")