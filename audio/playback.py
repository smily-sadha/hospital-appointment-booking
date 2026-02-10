import sounddevice as sd
import numpy as np


class AudioPlayer:
    def __init__(self, sample_rate: int = 24000):
        self.sample_rate = sample_rate

    def play(self, audio_bytes: bytes):
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
        sd.play(audio_np, samplerate=self.sample_rate)
        sd.wait()