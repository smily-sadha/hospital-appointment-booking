import os
import asyncio
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
assert GROQ_API_KEY, "Missing GROQ_API_KEY"


SYSTEM_PROMPT = (
    "You are a course lead qualification voice agent.\n"
    "Your role is to understand student interests, academic background, learning goals, and constraints.\n"
    "Classify the user's intent and qualification stage.\n\n"
    "Return ONLY a Python dictionary string like:\n"
    "{'intent': 'interested', 'stage': 'exploration'}\n\n"
    "Valid intents: interested, price_sensitive, needs_support, not_interested, unknown\n"
    "Valid stages: exploration, consideration, decision_ready"
)


class GroqLLM:
    """
    Async-compatible Groq client.
    Behavior is IDENTICAL to the previous version.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = model

    async def generate(self, prompt: str) -> str:
        """
        Non-blocking wrapper around Groq API.
        Runs the blocking SDK call in a thread executor.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._sync_generate,
            prompt
        )

    def _sync_generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

    # Backward compatibility (IMPORTANT)
    def __call__(self, prompt: str) -> str:
        """
        Allows existing synchronous code to keep working.
        """
        return self._sync_generate(prompt)
