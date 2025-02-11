import pyaudio

p = pyaudio.PyAudio()
default_input = p.get_default_input_device_info()
print("Default input device:")
print(default_input)
p.terminate()
