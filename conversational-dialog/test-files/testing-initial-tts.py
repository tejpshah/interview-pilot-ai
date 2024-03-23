"""

This file will just test out the 
OpenAI text-to-speech model so that
we have a POC of using it. 

"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() # Loading the key from the environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Weeeeeeeee"
)

response.stream_to_file("output2.mp3")

import pygame

# Initialize Pygame
pygame.init()

# Define the path to your MP3 file
mp3_file_path = 'output2.mp3'

# Load the MP3 file
pygame.mixer.music.load(mp3_file_path)

# Play the MP3 file
pygame.mixer.music.play()

# Wait for the MP3 file to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)  # Adjust the tick rate as needed

# Clean up Pygame resources
pygame.quit()