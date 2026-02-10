"""
STT Adapter
Ensures only FINAL transcripts reach the agent
"""

class STTAdapter:
    def __init__(self, stt_client, on_transcript):
        self.stt_client = stt_client
        self.on_transcript = on_transcript

    # -------------------------------

    async def start(self):
        """
        MUST be async because underlying STT is async
        """
        await self.stt_client.start(self._handle_result)

    # -------------------------------

    def _handle_result(self, transcript: str, is_final: bool):
        if is_final and transcript.strip():
            self.on_transcript(transcript)