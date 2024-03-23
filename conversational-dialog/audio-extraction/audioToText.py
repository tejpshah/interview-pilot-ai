import pyaudio
import wave
import whisper


class LiveSpeechToTextWhisper:
    def __init__(self, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=44100, record_seconds=5):
        self.chunk_size = chunk_size
        self.format = format
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
        self.audio_interface = pyaudio.PyAudio()
        self.stream = self.audio_interface.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)
        self.model = whisper.load_model("base")  # Choose model size as per your requirement

    def record_and_transcribe(self):
        print("* recording")
        frames = []
        try:
            for _ in range(0, int(self.rate / self.chunk_size * self.record_seconds)):
                try:
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    frames.append(data)
                except IOError as e:
                    # Handle the overflow error by ignoring the current chunk
                    print("Error recording data: ", e)
        finally:
            print("* done recording")

        # Save the recorded audio to a temporary file
        wf = wave.open("temp.wav", 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio_interface.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Load and transcribe the audio file
        result = self.model.transcribe("temp.wav")
        print("Transcription:", result["text"])

    def close(self):
        try:
            if self.stream.is_active():
                self.stream.stop_stream()
        except Exception as e:
            print("Error stopping stream: ", e)
        try:
            self.stream.close()
        except Exception as e:
            print("Error closing stream: ", e)
        self.audio_interface.terminate()


if __name__ == "__main__":
    lst = LiveSpeechToTextWhisper()
    try:
        lst.record_and_transcribe()
    finally:
        lst.close()