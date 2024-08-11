import cv2
import google.generativeai as genai
from text_to_speech import speak

def warn():
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
        generation_config = {"temperature": 1.5, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
        model = genai.GenerativeModel("gemini-1.5-pro", generation_config=generation_config)

        # Create prompt parts
        prompt_text = (
            "You are DIMA AI (Digital Image Mapping Assistant Artificial Intelligence), situated on a spectacle set equipped with a camera. "
            "Your purpose is to assist visually impaired individuals"
            "The image you are seeing is the blind person's POV. If he/she is in any danger like an approaching car or an obstacle or a pit in front of them, (even if someone is abou to harm them) please warn them"
            "If there is no danger, dont reply with anything. REMEBMER: only reply when the blind person is in danger. otherwise reply with '.'"
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
        warning =  response.text
        if warning == ".":
            return

    # If any errors, printing the errors
    else:
        print("DEBUG -- Error: Could not read frame from webcam.")
        cap.release()

# # Example usage
# ask_gemini("What is happening in the image?")
