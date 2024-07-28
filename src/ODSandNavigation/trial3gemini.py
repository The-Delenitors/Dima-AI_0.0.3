import google.generativeai as genai
import cv2
from PIL import Image
import numpy as np
import os
from gtts import gTTS
from playsound import playsound
import time
import json

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

# Function to parse the response from Gemini API
def parse_response(response_text):
    # This function assumes the response is a JSON-like string
    # Replace with actual parsing logic based on the response format
    try:
        response_data = json.loads(response_text)
        objects = []
        for item in response_data['predictions']:
            label = item['label']
            bbox = item['boundingBox']
            startX, startY, endX, endY = bbox['left'], bbox['top'], bbox['right'], bbox['bottom']
            objects.append({'label': label, 'bbox': [startX, startY, endX, endY]})
        return objects
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return []

# Start video capture and object detection
while True:
    start_time = time.time()
    
    ret, frame = cap.read()
    if not ret:
        break

    pil_image = convert_frame_to_pil(frame)

    # Send frame to Gemini API
    response = model.generate_content(["What is in this photo?", pil_image])

    # Process detection results
    objects = parse_response(response.text)

    for obj in objects:
        label = obj['label']
        startX, startY, endX, endY = obj['bbox']

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

    # Ensure smooth video feed
    end_time = time.time()
    elapsed_time = end_time - start_time
    sleep_time = max(1/30 - elapsed_time, 0)
    cv2.waitKey(int(sleep_time * 1000))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
