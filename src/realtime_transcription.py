import pyaudio
import numpy as np
from faster_whisper import WhisperModel

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

model = WhisperModel("base", device="cpu", compute_type="int8")

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("* リアルタイム文字起こしを開始します。Ctrl+Cで終了します。")

try:
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        segments, _ = model.transcribe(audio_data, language="ja")
        for segment in segments:
            print(segment.text)

except KeyboardInterrupt:
    print("* 文字起こしを終了します。")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
