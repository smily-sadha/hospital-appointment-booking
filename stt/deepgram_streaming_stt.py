"""
Deepgram Speech-to-Text (Turn-based)
"""

from deepgram import DeepgramClient, PrerecordedOptions


class DeepgramSTT:
    def __init__(self, api_key: str):
        self.client = DeepgramClient(api_key)

    def transcribe(self, audio_bytes: bytes) -> str:
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            language="en",
        )

        response = self.client.listen.prerecorded.v("1").transcribe_file(
            {
                "buffer": audio_bytes,
                "mimetype": "audio/wav",
            },
            options,
        )

        return (
            response["results"]["channels"][0]["alternatives"][0]["transcript"]
        )