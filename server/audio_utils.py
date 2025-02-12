import pyaudio


def create_audio_stream(callback):
    RATE = 16000
    CHUNK = 480  # webrtcvadが要求するサイズ制限
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=callback,
    )
    return stream
