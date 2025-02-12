import webrtcvad
import numpy as np


class VadWrapper:
    def __init__(self):
        self.vad = webrtcvad.Vad(3)  # Aggressiveness level: 0-3
        self.RATE = 16000
        self.CHUNK_SIZE = 480  # 必須: webrtcvad用フレームサイズ
        self.speech_buffer = []

    def is_speech(self, in_data):
        return self.vad.is_speech(in_data, self.RATE)

    def append_audio(self, in_data):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        self.speech_buffer.append(audio_data)

        if len(self.speech_buffer) > 20:  # 一定量収集後に結合して返す
            combined_audio = np.concatenate(self.speech_buffer)
            self.speech_buffer.clear()
            return combined_audio

        return None  # データがまだ不足している場合はNoneを返す
