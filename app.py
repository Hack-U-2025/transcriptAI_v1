from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from audio_input import AudioInput
from faster_whisper import WhisperModel
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

# WhisperモデルとAudioInputの初期化
model = WhisperModel("small", device="cpu", compute_type="int8")
audio_input = AudioInput()


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("start_transcription_unity")
def handle_start_transcription_unity():
    """
    Unityクライアントから「start_transcription_unity」イベントを受信した際に、
    音声入力を開始し、リアルタイムで文字起こし結果を送信する。
    """
    print("Starting transcription for Unity client...")
    try:
        audio_input.start_stream()
        while True:
            # 音声データを取得
            audio_chunk = audio_input.read_chunk()

            # faster-whisperモデルで文字起こし
            segments, _ = model.transcribe(audio_chunk)

            # 各セグメントをUnityクライアントに送信
            for segment in segments:
                socketio.emit("transcription_unity", {"text": segment.text})
    except Exception as e:
        print(f"Error during transcription: {e}")
        emit("error", {"message": str(e)})
    finally:
        audio_input.stop_stream()


@socketio.on("stop_transcription")
def handle_stop_transcription():
    """
    クライアントから「stop_transcription」イベントを受信した際に、
    音声入力と文字起こし処理を停止する。
    """
    print("Stopping transcription...")
    audio_input.stop_stream()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)
