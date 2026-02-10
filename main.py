"""
Hospital Appointment Booking Voice Agent
Deepgram STT + Deepgram TTS
Silence-based recording
"""

import os
import asyncio
from dotenv import load_dotenv

from hospital_agent.agent import HospitalAppointmentAgent
from memory.memory import ConversationMemory

from audio.recorder import SilenceRecorder
from audio.playback import AudioPlayer

from stt.deepgram_stt import DeepgramSTT
from tts.deepgram_tts import DeepgramTTS


# ------------------------------------------------------
# Environment
# ------------------------------------------------------

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    raise RuntimeError("DEEPGRAM_API_KEY not set in .env")


# ------------------------------------------------------
# Voice Agent
# ------------------------------------------------------

class HospitalVoiceAgent:
    def __init__(self):
        # ----------------------------
        # Memory
        # ----------------------------
        self.memory = ConversationMemory()
        self.memory.start_session("hospital_session_001")

        # ----------------------------
        # Core Agent
        # ----------------------------
        self.agent = HospitalAppointmentAgent(
            memory=self.memory
        )

        # ----------------------------
        # Audio + STT + TTS
        # ----------------------------
        self.recorder = SilenceRecorder(
            start_timeout_ms=5000,
            silence_threshold=350.0,
            silence_duration_ms=900,
            max_record_ms=12000,
        )

        self.stt = DeepgramSTT(DEEPGRAM_API_KEY)
        self.tts = DeepgramTTS(DEEPGRAM_API_KEY)
        self.player = AudioPlayer(sample_rate=24000)

        # ----------------------------
        # Conversation control
        # ----------------------------
        self.no_response_count = 0

    # --------------------------------------------------

    async def speak(self, text: str):
        print(f"\n🤖 AGENT: {text}")
        audio = self.tts.synthesize(text)
        self.player.play(audio)

    # --------------------------------------------------

    async def listen_and_transcribe(self) -> str:
        """
        Record user speech → STT → text
        """
        print("🎙️ Listening for user speech...")
        audio_bytes = self.recorder.record()

        print("🧠 Transcribing user speech...")
        transcript = self.stt.transcribe(audio_bytes)

        transcript = transcript.strip()
        if transcript:
            print(f"📝 STT RESULT: {transcript}")
        else:
            print("📝 STT RESULT: <empty>")

        return transcript

    # --------------------------------------------------

    async def run(self):
        print("=" * 60)
        print("🏥 Hospital Appointment Booking Voice Agent")
        print("=" * 60)

        # Agent starts the call
        await self.speak(
            "Hello, this is the hospital appointment desk. "
            "How may I help you today?"
        )

        while True:
            user_text = await self.listen_and_transcribe()

            # --------------------------------
            # USER DID NOT SPEAK
            # --------------------------------
            if not user_text:
                self.no_response_count += 1

                if self.no_response_count == 1:
                    await self.speak("Hello, can you hear me?")
                    continue

                if self.no_response_count == 2:
                    await self.speak("No worries if now is not a good time.")
                    continue

                if self.no_response_count >= 3:
                    await self.speak(
                        "I will end this call for now. "
                        "Please feel free to reach out again."
                    )
                    print("👋 Call ended due to no response.")
                    break

            # --------------------------------
            # USER SPOKE
            # --------------------------------
            self.no_response_count = 0
            print(f"\n👤 HUMAN: {user_text}")

            response = self.agent.handle_input(user_text)
            await self.speak(response)


# ------------------------------------------------------
# Entrypoint
# ------------------------------------------------------

if __name__ == "__main__":
    try:
        asyncio.run(HospitalVoiceAgent().run())
    except KeyboardInterrupt:
        print("\n👋 Call ended.")
