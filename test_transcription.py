from faster_whisper import WhisperModel

# モデルの初期化
model = WhisperModel("small", device="cpu")

# テスト用音声ファイル（適宜パスを変更）
audio_path = "test_audio.wav"

# 音声ファイルの文字起こし
segments, info = model.transcribe(audio_path)

print(f"Detected language: {info.language} (Probability: {info.language_probability})")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
