from faster_whisper import WhisperModel

# "small"モデルを選択し、CPUで動作するよう設定
# CPU環境で動作するよう設定
model = WhisperModel("small", device="cpu", compute_type="int8")

print("Model downloaded and ready to use.")
