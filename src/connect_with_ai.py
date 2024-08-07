import cv2
import google.generativeai as genai
from text_to_speech import speak

def ask_gemini(user_prompt_command):
    # Capture an image from the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("DEBUG -- Error: Could not open webcam.")
        exit()

    ret, frame = cap.read()
    if ret:
        # Display the captured image
        cv2.imshow('DEBUG -- Captured Image', frame)
        cv2.waitKey(5000)  # Wait for 5 seconds
        cv2.destroyAllWindows()

        # Convert the frame to image bytes
        _, img_encoded = cv2.imencode('.jpg', frame)
        image_bytes = img_encoded.tobytes()
        cap.release()

        # Configure Google Generative AI
        api_key = "AIzaSyCi5EYAd8kASk2UQG-BZAIugmOHieQmLUw"  # Replace with your actual API key
        genai.configure(api_key=api_key)
        generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
        model = genai.GenerativeModel("gemini-1.5-pro", generation_config=generation_config)

        # Create prompt parts
        prompt_text = (
            "You are DIMA AI (Digital Image Mapping Assistant Artificial Intelligence), situated on a spectacle set equipped with a camera. "
            "Your purpose is to assist visually impaired individuals. The statement in quotes (e.g. 'what is your name' which you reply "
            "telling that you are Dima AI which helps you(you in the sense blind person)) is what a blind person is asking you. If the question is not "
            "related to the image attached, please indicate that the image does not contain relevant information and answer the question asked or basically act like an assistant."
            "If there is text in the image, provide a transcription. "
            "The blind person asks: '{}'\n".format(user_prompt_command)
        )
        
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }

        print("DEBUG -- Thinking")
        speak("Thinking")

        # Generate content
        response = model.generate_content([prompt_text, image_part])

        # Print the response
        print(response.text)
        speak(response.text)

    # If any errors, printing the errors
    else:
        print("DEBUG -- Error: Could not read frame from webcam.")
        speak("Could not read frame from webcam.")
        cap.release()

# # Example usage
# ask_gemini("What is happening in the image?")
