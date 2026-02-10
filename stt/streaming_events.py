from dataclasses import dataclass

@dataclass
class PartialTranscript:
    text: str

@dataclass
class FinalTranscript:
    text: str
    language: str