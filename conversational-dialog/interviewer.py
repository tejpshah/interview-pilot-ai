"""

This class will represent the conversational
agent (the interviewer)

"""
# Importing libraries 
from openai import OpenAI
from dotenv import load_dotenv
import os
import pygame

class Interviewer:
    # Constructor
    def __init__(self):
        # Creating the OpenAI client
        load_dotenv() # Loading the key from the environment
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Function for speech to text
    def text_to_speech(self,text:str):
        speech = self.client.audio.speech.create(
            model='tts-1',
            voice='alloy',
            input=text
        )
        speech.stream_to_file("interviewer-speech.mp3")

        # Playing the audio
        pygame.init()
        pygame.mixer.music.load("interviewer-speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.quit()   
    # Function for text-to-text -> NEEDED

    # Function for Speech-to-text -> Need to add


# Main Method for testing
if __name__ == '__main__':
    # Creating the object
    interviewer = Interviewer()
    interviewer.text_to_speech('I like trains')