"""
Deepgram Text-to-Speech
REST streaming (deepgram-sdk 3.2.4)
Audio is delivered ONLY via response.stream
"""

from deepgram import DeepgramClient, SpeakOptions


class DeepgramTTS:
    def __init__(self, api_key: str):
        self.client = DeepgramClient(api_key)

    def synthesize(self, text: str) -> bytes:
        """
        Convert text to speech and return raw PCM audio bytes
        """
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            sample_rate=24000,
        )

        response = self.client.speak.v("1").stream(
            {"text": text},
            options
        )

        # ✅ AUDIO IS ONLY IN response.stream
        audio_bytes = b""

        for chunk in response.stream:
            if isinstance(chunk, (bytes, bytearray)):
                audio_bytes += chunk

        if not audio_bytes:
            raise RuntimeError("Deepgram TTS returned empty audio stream")

        return audio_bytes
