import asyncio
import json
from websockets import serve
from audio_utils import create_audio_stream
from whisper_utils import WhisperModelWrapper
from vad_utils import VadWrapper

# 設定ファイル読み込み
with open("config.json", "r") as f:
    config = json.load(f)

HOST = config["host"]
PORT = config["port"]


class RealTimeTranscriptionServer:
    def __init__(self):
        self.vad = VadWrapper()
        self.whisper = WhisperModelWrapper()
        self.audio_queue = asyncio.Queue()

    async def transcribe_audio(self, websocket):
        while True:
            audio_data = await self.audio_queue.get()
            segments = self.whisper.transcribe(audio_data)
            for segment in segments:
                await websocket.send(segment.text)

    def process_audio(self, in_data, frame_count, time_info, status):
        if self.vad.is_speech(in_data):
            audio_data = self.vad.append_audio(in_data)
            if audio_data is not None:
                asyncio.run_coroutine_threadsafe(
                    self.audio_queue.put(audio_data), asyncio.get_event_loop()
                )
        return (in_data, pyaudio.paContinue)

    async def handler(self, websocket, path):
        print("クライアントが接続されました")
        stream = create_audio_stream(self.process_audio)
        stream.start_stream()
        try:
            await self.transcribe_audio(websocket)
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            stream.stop_stream()
            stream.close()


# サーバー起動
async def main():
    server = RealTimeTranscriptionServer()
    async with serve(server.handler, HOST, PORT):
        print(f"サーバーが起動しました: ws://{HOST}:{PORT}")
        await asyncio.Future()  # サーバーを停止しないため


asyncio.run(main())
