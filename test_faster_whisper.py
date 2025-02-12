from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu")
segments, info = model.transcribe("path_to_audio_file.wav")

print("Detected language:", info.language)
for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
