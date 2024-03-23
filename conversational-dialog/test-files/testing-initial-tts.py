"""

This file will just test out the 
OpenAI text-to-speech model so that
we have a POC of using it. 

"""
from openai import OpenAI

# Creating the client
client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello world! This is a streaming test.",
)

response.stream_to_file("output.mp3")