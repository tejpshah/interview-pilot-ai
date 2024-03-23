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
import sys 

sys.path.append('audio-extraction')
from audioToText import AudioRecorder
from audioToText import transcribe_audio


class Interviewer:
    # Constructor
    def __init__(self):
        # Creating the OpenAI client
        load_dotenv() # Loading the key from the environment
        self.client_openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.client_claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        # Managing the history of conversation
        self.history = []

        # Creating the recorder object
        self.recorder = AudioRecorder()
    
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
    def speech_to_text(self):
        frames = self.recorder.record_until_silence()
        wav_filename = self.recorder.save_recording(frames)
        text = transcribe_audio(wav_filename)

        # Optionally, remove the WAV file if it's no longer needed
        os.remove(wav_filename)

        return text
    
    # Putting the agent together
    def main(self):
        initial_text = self.speech_to_text()

        # Getting response
        self.text_to_text(initial_text)

        # Say the response
        self.text_to_speech(self.history[-1]['content'])


# Main Method for testing
if __name__ == '__main__':
    # Creating the object
    interviewer = Interviewer()
    interviewer.main()