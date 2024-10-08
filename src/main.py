from text_to_speech import speak
from speech_to_text import listen
from connect_with_ai import ask_gemini
from navigation import navigate
from greet import greet
from warning import warn

def start():
    print("DEBUG -- Initializing...")
    speak("Digital image mapping assistant artificial intelligence is starting. Please wait a moment.")

    while True:
        # Resetting prompts
        user_promt = "."
        user_promt_command = "."
        # Listening for wake word
        print("DEBUG -- Waiting for wake-word")
        user_promt = listen()
        # Displaying what the user said
        print("DEBUG -- User said:"+user_promt)

        # Checking if the user said the wake word
        if any(word in user_promt.lower() for word in ["dima", "dayma", "deema", "daima", "dheema", "dhima", "dema", "computer"]):
            # Greeting the user if the wake word is detected
            print("DEBUG -- Wake word detected. Say your command")
            greet()

            # Listening for command
            user_promt_command = listen()
            print("DEBUG -- User said:"+user_promt_command)

            # Navigation mode
            if any(word in user_promt_command.lower() for word in ["activate navigation mode", "turn on navigation mode", "navigation mode", "navigation", "activate navigation"]):
                speak("Navigation mode is activating.")
                print("DEBUG -- Navigation mode is activating")

                # Starting navigation loop
                while True:
                    # Listening for navigation commands
                    user_navigation_prompt = listen()
                    print("DEBUG -- User said:"+user_navigation_prompt)

                    # Checking if the user wants to cancel navigation mode
                    if any(word in user_navigation_prompt.lower() for word in ["cancel", "stop", "exit", "quit"]):
                        print("DEBUG -- Cancel command detected.")  
                        speak("Exiting navigation maode")
                        break

                    # sending user comand to gemini for navigation   
                    navigate(user_navigation_prompt)

            # Checking if the user wants to cancel or stop the program
            elif any(phrase in user_promt_command.lower() for phrase in ["stop program", "exit program", "quit program", "close program", "top program"]):
                print("DEBUG -- Stop command detected. Exiting...")
                speak("ok")
                break  
            elif any(word in user_promt_command.lower() for word in ["cancel", "stop", "exit", "quit"]):
                print("DEBUG -- Cancel command detected.")
                speak("Ok.")
                continue
            elif user_promt_command == ("."):
                continue            

            # Sending the command to gemini
            ask_gemini(user_promt_command)
        
        # Checking if the user is in danger
        warn()
            
    # Stopping program
    print("DEBUG -- Stopping program...")
    speak("Digital image mapping assistant artificial intelligence is closing. Thank you.")
  
# Starting the program
if __name__ == "__main__":
    start()