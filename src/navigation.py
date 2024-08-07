import cv2
import google.generativeai as genai
from text_to_speech import speak

def navigate(user_navigation_prompt = "Guide me. The attached image is what is in fron of me. Please tell me where to go"):
    # Capture an image from the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("DEBUG -- Error: Could not open webcam.")
        exit()

    ret, frame = cap.read()
    if ret:
        # Display the captured image
        cv2.imshow('DEBUG -- Captured Image', frame)
        cv2.waitKey(1) 
        cv2.destroyAllWindows()

        # Convert the frame to image bytes
        _, img_encoded = cv2.imencode('.jpg', frame)
        image_bytes = img_encoded.tobytes()
        cap.release()

        # Configure Google Generative AI
        api_key = "AIzaSyCi5EYAd8kASk2UQG-BZAIugmOHieQmLUw"  # Replace with your actual API key
        genai.configure(api_key=api_key)
        generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
        model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

        # Create prompt parts
        prompt_text = (
            "You are DIMA AI (Digital Image Mapping Assistant Artificial Intelligence), situated on a spectacle set equipped with a camera. "
            "Your purpose is to assist visually impaired individuals in navigation. Avoid giving multiple instructions at once (max 4)"
            "The statement in quotes (e.g. 'abcabc') is what the blind person is asking you"
            "Give commands to the blind person like go forward, turn left, turn right, stop, etc. Give only necessary info."
            "The blind person asks: '{}'\n".format(user_navigation_prompt)
        )
        
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }

        print("DEBUG -- Thinking")

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

# navigate("Take me out of this room")
