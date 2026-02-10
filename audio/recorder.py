"""
Audio Recorder with Silence Detection (WAV output)
-------------------------------------------------

Records microphone input until silence is detected
and returns proper WAV bytes (with header).

This FIXES Deepgram empty transcription.
"""

import sounddevice as sd
import numpy as np
import time
import io
import wave


class SilenceRecorder:
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_ms: int = 100,
        silence_threshold: float = 350.0,
        silence_duration_ms: int = 900,
        max_record_ms: int = 10000,
        start_timeout_ms: int = 5000,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_ms = chunk_ms
        self.chunk_samples = int(sample_rate * chunk_ms / 1000)

        self.silence_threshold = silence_threshold
        self.silence_duration_ms = silence_duration_ms
        self.max_record_ms = max_record_ms
        self.start_timeout_ms = start_timeout_ms

    # --------------------------------------------------

    def _rms(self, audio: np.ndarray) -> float:
        return np.sqrt(np.mean(np.square(audio.astype(np.float32))))

    # --------------------------------------------------

    def record(self) -> bytes:
        print("🎙️ Listening for user speech...")

        audio_chunks = []
        silence_ms = 0
        total_ms = 0
        speech_detected = False

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.chunk_samples,
        ) as stream:

            while True:
                audio_chunk, _ = stream.read(self.chunk_samples)
                audio_chunks.append(audio_chunk.copy())

                rms = self._rms(audio_chunk)
                total_ms += self.chunk_ms

                if rms > self.silence_threshold:
                    speech_detected = True
                    silence_ms = 0
                else:
                    if speech_detected:
                        silence_ms += self.chunk_ms

                if speech_detected and silence_ms >= self.silence_duration_ms:
                    print("🛑 Silence detected, stopping recording.")
                    break

                if not speech_detected and total_ms >= self.start_timeout_ms:
                    print("⏱️ No speech detected, stopping.")
                    break

                if total_ms >= self.max_record_ms:
                    print("⏱️ Max recording time reached.")
                    break

        print("✅ Recording complete.")

        audio_np = np.concatenate(audio_chunks, axis=0)

        # 🔥 CONVERT TO WAV BYTES (CRITICAL FIX)
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # int16 = 2 bytes
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_np.tobytes())

        return wav_buffer.getvalue()