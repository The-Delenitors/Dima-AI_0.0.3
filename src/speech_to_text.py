import speech_recognition as sr
from text_to_speech import speak
from mp3play import alert
# Function to listen to the user's voice
def listen():
    # Defining microphones
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Listen
    with microphone as source:
        print("DEBUG -- Listening...")
        alert(1)
        # Adjust for ambient noise levels
        recognizer.adjust_for_ambient_noise(source)
        # Capture the audio input
        audio = recognizer.listen(source)

    # Recognising
    try:
        print("DEBUG -- Recognizing...")
        alert(2)
        # Convert speech to text
        text = recognizer.recognize_google(audio)
        return text
    
    # If any errors, printing the errors
    except sr.UnknownValueError:
        print("DEBUG -- Sorry, I could not understand your audio.")
        alert(0)
        return  "."
    
    except sr.RequestError:
        print("DEBUG -- Could not request results; check your network connection.")
        alert(0)
        speak("Could not request results; check your network connection.")
        return "."
