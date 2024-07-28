import google.generativeai as genai
import cv2
from PIL import Image
import numpy as np
import os
from gtts import gTTS
from playsound import playsound

# Configure the Gemini API
api_key = "AIzaSyCi5EYAd8kASk2UQG-BZAIugmOHieQmLUw"  # Replace with your actual API key
genai.configure(api_key=api_key)
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)


# Initialize video capture
cap = cv2.VideoCapture(0)

# Function to play warning sound and speak the distance
def alert_user(distance):
    warning_text = f"Warning! Object detected at {distance} centimeters."
    tts = gTTS(text=warning_text, lang='en')
    tts.save("warning.mp3")
    playsound("warning.mp3")
    os.remove("warning.mp3")

# Function to convert OpenCV frame to PIL Image
def convert_frame_to_pil(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    return pil_image

# Start video capture and object detection
ret, frame = cap.read()
if not ret:
    cap.release()
    cv2.destroyAllWindows()
    raise Exception("Could not read frame from webcam.")

pil_image = convert_frame_to_pil(frame)

# Send frame to Gemini API
response = model.generate_content(["What is in this photo?", pil_image])

# Process detection results (assuming response.text contains the label and possibly the bounding box info)
print(response.text)  # Replace with actual parsing of the response to get labels and bounding boxes

# Here you should parse the response.text to extract bounding box information and object labels
# Since the response format is not specified, this part is left abstract
# Example (pseudo-code):
# objects = parse_response(response.text)
# Replace this with the actual response parsing
objects = []  # Replace with actual parsing logic

# Example of hardcoded parsing logic (for illustration purposes only)
# objects = [
#     {"label": "person", "bbox": [50, 50, 200, 200]},
#     {"label": "cat", "bbox": [250, 250, 400, 400]}
# ]

for obj in objects:
    label = obj['label']
    startX, startY, endX, endY = obj['bbox']  # Replace with actual keys from parsed response

    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Assuming the camera is calibrated and using a known focal length and object width for distance calculation
    known_width = 15.0  # example known width in cm
    focal_length = 700  # example focal length in pixels
    object_width_in_frame = endX - startX
    distance = (known_width * focal_length) / object_width_in_frame

    cv2.putText(frame, f'{label}: {round(distance, 2)} cm', (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Alert if the object is within 10 cm
    if distance < 10:
        alert_user(round(distance, 2))

cv2.imshow('Object Detection', frame)
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
