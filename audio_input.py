import pyaudio
import numpy as np


class AudioInput:
    def __init__(self, chunk=1024, format=pyaudio.paFloat32, channels=1, rate=16000):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self):
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )
        print("Audio stream started")

    def read_chunk(self):
        if self.stream is None:
            raise ValueError("Stream is not started")
        data = self.stream.read(self.chunk)
        return np.frombuffer(data, dtype=np.float32)

    def stop_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        print("Audio stream stopped")


if __name__ == "__main__":
    audio_input = AudioInput()
    audio_input.start_stream()
    try:
        print("Recording. Press Ctrl+C to stop.")
        while True:
            audio_chunk = audio_input.read_chunk()
            print(f"Recorded chunk with max amplitude: {np.max(np.abs(audio_chunk))}")
    except KeyboardInterrupt:
        print("Stopping recording")
    finally:
        audio_input.stop_stream()
