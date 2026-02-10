"""
TTS Adapter - Abstract interface for text-to-speech services
"""

import asyncio
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()


class TTSAdapter(ABC):
    """Abstract base class for TTS implementations"""
    
    @abstractmethod
    async def synthesize(self, text: str, language: str = "en") -> bytes:
        """
        Synthesize text to audio bytes.
        
        Args:
            text: Text to synthesize
            language: Language code (default: 'en')
            
        Returns:
            Audio bytes (PCM format)
        """
        raise NotImplementedError


class SimpleTTS(TTSAdapter):
    """Simple TTS using Google TTS (requires gtts library)"""
    
    async def synthesize(self, text: str, language: str = "en") -> bytes:
        """
        Synthesize using Google TTS.
        """
        # Placeholder - requires: pip install gtts
        # from gtts import gTTS
        # tts = gTTS(text=text, lang=language, slow=False)
        # tts.save('temp.mp3')
        # with open('temp.mp3', 'rb') as f:
        #     return f.read()
        
        print(f"[TTS] Synthesizing: {text[:50]}...")
        return b""  # Empty bytes for now


class PlaybackMixin:
    """Mixin to add playback functionality to TTS adapters"""
    
    async def synthesize_and_play(self, text: str, player, language: str = "en"):
        """Synthesize text and play audio"""
        audio = await self.synthesize(text, language)
        if audio:
            player.play(audio)