import pyaudio
import speech_recognition as sr


class LiveSpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen_and_recognize(self):
        # Adjust the recognizer sensitivity to ambient noise
        with self.microphone as source:
            print("Adjusting for ambient noise. Please wait...")
            self.recognizer.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(self.recognizer.energy_threshold))

        # Start listening and recognizing
        print("Listening...")
        try:
            with self.microphone as source:
                while True:
                    audio = self.recognizer.listen(source)
                    print("Recognizing...")
                    try:
                        # Recognize speech using Google Web Speech API
                        text = self.recognizer.recognize_google(audio)
                        print("You said: {}".format(text))
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {e}")
        except KeyboardInterrupt:
            print("Exiting...")


if __name__ == "__main__":
    lst = LiveSpeechToText()
    lst.listen_and_recognize()
