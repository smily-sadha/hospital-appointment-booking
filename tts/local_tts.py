"""
Local TTS using pyttsx3
Low latency, offline, stable
"""

import pyttsx3


class LocalTTS:
    def __init__(self, rate: int = 170):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)

    async def synthesize(self, text: str):
        """
        Async-compatible generator
        """
        self.engine.say(text)
        self.engine.runAndWait()
        yield b""  # keep async interface consistent
