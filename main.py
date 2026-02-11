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
        self.memory = ConversationMemory()
        self.memory.start_session("hospital_session_001")

        self.agent = HospitalAppointmentAgent(memory=self.memory)

        self.recorder = SilenceRecorder(
            start_timeout_ms=5000,
            silence_threshold=350.0,
            silence_duration_ms=900,
            max_record_ms=12000,
        )

        self.stt = DeepgramSTT(DEEPGRAM_API_KEY)
        self.tts = DeepgramTTS(DEEPGRAM_API_KEY)
        self.player = AudioPlayer(sample_rate=24000)

        self.no_response_count = 0

    # --------------------------------------------------

    async def speak(self, text: str):
        """
        Speak text with precise sentence-level pauses
        """
        print(f"\n🤖 AGENT: {text}")

        lower = text.lower()
        trigger = "let me check the availability"

        if trigger in lower:
            # Find the end of the sentence that contains the trigger
            start = lower.find(trigger)
            sentence_end = text.find(".", start)

            if sentence_end != -1:
                sentence_end += 1  # include the period

                first_sentence = text[:sentence_end].strip()
                remaining_text = text[sentence_end:].strip()

                # 1️⃣ Speak the full acknowledgment sentence
                audio = self.tts.synthesize(first_sentence)
                self.player.play(audio)

                # ⏱️ 1-second pause AFTER sentence completion
                await asyncio.sleep(1)

                # 2️⃣ Speak the remaining content (if any)
                if remaining_text:
                    audio = self.tts.synthesize(remaining_text)
                    self.player.play(audio)

                return

        # Default behavior
        audio = self.tts.synthesize(text)
        self.player.play(audio)

    # --------------------------------------------------

    async def listen_and_transcribe(self) -> str:
        print("🎙️ Listening for user speech...")
        audio_bytes = self.recorder.record()

        print("🧠 Transcribing user speech...")
        transcript = self.stt.transcribe(audio_bytes).strip()

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

        await self.speak(
            "Hello, this is the hospital appointment desk. "
            "How may I help you today?"
        )

        while True:
            user_text = await self.listen_and_transcribe()

            if not user_text:
                self.no_response_count += 1

                if self.no_response_count == 1:
                    await self.speak("Hello, can you hear me?")
                    continue

                if self.no_response_count >= 2:
                    print("👋 Call ended.")
                    break

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
