"""

This class will represent the conversational
agent (the interviewer)

"""
# Importing libraries 
import os
import threading
from dotenv import load_dotenv
import pygame
from openai import OpenAI
import anthropic

# Assuming audioToText.py is correctly set up in the sys.path.append('audio-extraction') directory
from audioToText import AudioRecorder, transcribe_audio

class Interviewer:
    def __init__(self,persona):
        load_dotenv()
        self.client_openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.client_claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.history = []
        self.recorder = AudioRecorder()
        pygame.mixer.init()
        self.playback_finished = threading.Event()

        # Appending the initial persona
        self.persona = persona

    def text_to_speech(self, text: str):
        try:
            speech = self.client_openai.audio.speech.create(model='tts-1', voice='alloy', input=text)
            speech.stream_to_file("interviewer-speech.mp3")
        except Exception as e:
            print(f"Error generating speech: {e}")
            return

        def play_audio():
            try:
                pygame.mixer.music.load("interviewer-speech.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print(f"Error playing audio: {e}")
            finally:
                self.playback_finished.set()

        threading.Thread(target=play_audio).start()
        self.playback_finished.wait()  # Wait here until audio playback is finished

    def text_to_text(self, input_text: str):
        try:
            self.history.append({'role': 'user', 'content': input_text})
            response = self.client_claude.messages.create(
                model='claude-3-haiku-20240307', max_tokens=1000,
                temperature=0, system_prompt=self.persona,messages=self.history
            )
            response_text = response.content[0].text
            self.history.append({'role': 'assistant', 'content': response_text})
            return response_text
        except Exception as e:
            print(f"Error in text-to-text conversion: {e}")
            return "I'm sorry, I didn't catch that."

    def speech_to_text(self):
        self.playback_finished.clear()  # Ensure this is reset before starting playback
        frames = self.recorder.record_until_silence()
        wav_filename = self.recorder.save_recording(frames)
        try:
            text = transcribe_audio(wav_filename)
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            text = ""
        finally:
            os.remove(wav_filename)
        return text

    def main(self):
        done = False
        while not done:
            self.playback_finished.set()  # Assume playback is finished at the start
            user_speech = self.speech_to_text()

            if user_speech.strip().lower() == 'i am done':
                done = True
                continue

            response_text = self.text_to_text(user_speech)
            self.text_to_speech(response_text)

if __name__ == '__main__':
    # Adding the persona
    with open('test-persona-prompt.txt','r') as file:
        persona = file.read()
    interviewer = Interviewer(persona)
    interviewer.main()
