import cv2
import base64
import requests  # Assuming Gemini API uses HTTP requests
from text_to_speech import speak

# Initialize your Gemini API client here
GEMINI_API_URL = 'https://api.gemini.example/analyze'  # Replace with actual URL
API_KEY = 'your_gemini_api_key'  # Replace with your actual API key

def ask_gemini_with_image(user_prompt_command):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("DEBUG -- Error: Could not open webcam.")
        exit()

    ret, frame = cap.read()

    if ret:
        # Display the captured image
        cv2.imshow('DEBUG -- Captured Image', frame)
        
        # Wait for a key press and close the window after 2 seconds (2000 milliseconds)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        # Convert the frame to base64 encoding
        _, img_encoded = cv2.imencode('.jpg', frame)
        image_bytes = img_encoded.tobytes()
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        cap.release()
        print("DEBUG -- Thinking...")
        speak("Thinking")

        try:
            # Construct payload for Gemini API
            payload = {
                'api_key': API_KEY,
                'image_base64': image_b64,
                'prompt': user_prompt_command
            }

            # Make a POST request to Gemini API
            response = requests.post(GEMINI_API_URL, json=payload)

            # Check if request was successful
            if response.status_code == 200:
                # Get the description from Gemini's response
                response_data = response.json()
                responce_from_gemini = response_data['description']  # Adjust key as per API response

                print(f"DEBUG -- Response from Gemini: {responce_from_gemini}")

                # Speak the description using the text-to-speech engine
                speak(responce_from_gemini)
            else:
                print(f"API Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"HTTP Request Error: {e}")

    else:
        print("Error: Could not capture an image.")

# Example usage
# ask_gemini_with_image("what is in front of me?")
