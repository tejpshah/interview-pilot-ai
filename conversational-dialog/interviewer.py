"""

This class will represent the conversational
agent (the interviewer)

"""
# Importing libraries 
from openai import OpenAI
from dotenv import load_dotenv
import os
import pyaudio
from io import BytesIO
import numpy as np

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
        return speech.content
    
    # Function for text-to-text -> NEEDED

    # Function for Speech-to-text -> Need to add
    
def stream_audio(audio_bytes):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=25000,
                    output=True)
    audio_array = audio_bytes.getbuffer().tobytes()
    stream.write(audio_array)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Main Method for testing
if __name__ == '__main__':
    # Creating the object
    interviewer = Interviewer()
    test = interviewer.text_to_speech('I like trains')
    stream_audio(BytesIO(test))
    print('Yeet')