import asyncio
import websockets
import numpy as np
import pyaudio
from faster_whisper import WhisperModel

# Whisperモデルのロード
model = WhisperModel("base", device="cpu")

# マイク入力の設定
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# WebSocketサーバーの設定
HOST = "localhost"
PORT = 8765


async def transcribe(websocket, path):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("マイク入力開始")

    try:
        while True:
            data = stream.read(CHUNK)
            audio_data = (
                np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            )
            segments, _ = model.transcribe(audio_data, beam_size=5)
            for segment in segments:
                await websocket.send(segment.text)
    except websockets.ConnectionClosed:
        print("クライアントとの接続が閉じられました")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


start_server = websockets.serve(transcribe, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
