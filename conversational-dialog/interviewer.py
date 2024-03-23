"""

This class will represent the conversational
agent (the interviewer)

"""
# Importing libraries 
from openai import OpenAI
import anthropic
from dotenv import load_dotenv
import os
import pygame

class Interviewer:
    # Constructor
    def __init__(self):
        # Creating the OpenAI client
        load_dotenv() # Loading the key from the environment
        self.client_openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.client_claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        # Managing the history of conversation
        self.history = []
    
    # Function for speech to text
    def text_to_speech(self,text:str):
        speech = self.client_openai.audio.speech.create(
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
    def text_to_text(self,input_text:str):
        self.history.append({'role':'user','content':input_text})

        text_output = self.client_claude.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=1000,
            temperature=0,
            messages=self.history
        )
        self.history.append({'role':'assistant','content':text_output.content[0].text})
        return text_output.content[0].text

    # Function for Speech-to-text -> Need to add


# Main Method for testing
if __name__ == '__main__':
    # Creating the object
    interviewer = Interviewer()
    # interviewer.text_to_speech('I like trains')
    input_text = 'Hello there!'

    while input_text != 'Exit':
        print(interviewer.text_to_text(input_text))
        input_text = input()