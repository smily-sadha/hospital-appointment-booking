# 🎓 Course Lead Qualification Voice Agent

A voice-based conversational AI agent that qualifies education leads through intelligent dialogue.

## 🎯 Features

✅ **Voice Input/Output** - Real-time audio conversation  
✅ **Intent Recognition** - Detects student interests, objections, and readiness  
✅ **Policy Engine** - Enforces qualification rules (no early selling, respects decision authority)  
✅ **State Management** - Tracks lead profile, constraints, and qualification stage  
✅ **Multi-language Support** - Supports English, Hindi, Tamil, Telugu, Kannada, Malayalam  
✅ **Memory & Context** - Maintains conversation history per session  
✅ **Async Architecture** - Non-blocking audio processing  

---

## 📋 Project Structure

```
course-lead-qualification-agent/
├── agent/              # Core agent logic
│   ├── agent.py        # Main orchestration
│   ├── state.py        # Lead state model
│   ├── intent.py       # Intent classification
│   ├── policy_engine.py # Qualification rules
│   ├── router.py       # Action routing
│   ├── slots.py        # Slot definitions
│   └── response_template.py # Response templates
│
├── llm/                # Language models
│   └── groq_client.py  # Groq LLM integration
│
├── stt/                # Speech-to-text
│   ├── stt_adapter.py          # Abstract interface
│   ├── deepgram_stt.py         # Deepgram STT
│   ├── deepgram_streaming_stt.py # Streaming STT
│   └── streaming_events.py     # Event types
│
├── tts/                # Text-to-speech
│   ├── tts_adapter.py  # Abstract interface
│   └── voice_map.py    # Voice configurations
│
├── audio/              # Audio I/O
│   ├── recorder.py     # Audio recording
│   └── playback.py     # Audio playback
│
├── memory/             # Session memory
│   └── memory.py       # Conversation history
│
├── language/           # Language processing
│   ├── detect_language.py
│   ├── indic_phonetic.py
│   └── roman_to_native.py
│
├── tests/              # Test suite
│   ├── test_lead_qualification.py
│   └── test_agent_flow.py
│
├── main.py             # Voice agent entry point
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

---

## 🚀 Quick Start

### 1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 2. **Configure Environment**

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=your_groq_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
```

### 3. **Run the Voice Agent**

```bash
python main.py
```

The agent will:
- Listen for voice input (5 seconds)
- Transcribe using Deepgram
- Process through qualification logic
- Generate response
- Play back (TTS support coming)

---

## 🔄 Agent Flow

```
User speaks
    ↓
[STT] Deepgram transcribes audio
    ↓
[AGENT] Detects intent from text
    ↓
[STATE] Updates lead profile
    ↓
[POLICY] Decides next action based on rules
    ↓
[ROUTER] Maps action to response template
    ↓
[RESPONSE] Renders personalized message
    ↓
[MEMORY] Stores in conversation history
    ↓
[TTS] Synthesizes speech (audio playback)
```

---

## 💡 Key Concepts

### **Intent Recognition**
- `INTERESTED` - Clear curiosity or engagement
- `PARTIALLY_INTERESTED` - Exploring, early-stage
- `PRICE_SENSITIVE` - Cost concerns
- `NEEDS_DECISION_SUPPORT` - Parents/guardians involved
- `NOT_INTERESTED` - Explicit disinterest
- `READY_FOR_COUNSELLOR` - Wants to talk to admissions

### **Policy Engine Rules**
- **No early selling** - Never push pricing or urgency
- **Qualification-first** - Gather information before handoff
- **Respect decision authority** - Different handling for 18+ vs. parent-dependent
- **Soft on objections** - Empathetic handling of concerns

### **Lead State Tracking**
- Academic background (student/working)
- Experience level (beginner/intermediate)
- Course interest (AI, ML, etc.)
- Learning goal (exploration/build/career)
- Budget sensitivity (high/medium/low)
- Timeline (now/later/unclear)
- Decision maker (self/parents)

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

Test cases cover:
- ✅ Exploratory student flow (no handoff until qualified)
- ✅ Price-sensitive lead handling (no pressure)
- ✅ Not-interested exit (polite, no follow-up)
- ✅ Counsellor handoff (only when fully qualified)
- ✅ Parent decision authority (special handling)

---

## 🔧 Configuration

### Audio Settings
```python
SAMPLE_RATE = 16000  # Deepgram nova-2 expects 16kHz
RECORDING_DURATION = 5  # seconds per turn
```

### LLM Settings
```python
MODEL = "llama-3.1-8b-instant"  # Groq
TEMPERATURE = 0.2  # Conservative responses
```

### TTS Voices
```python
VOICE_MAP = {
    "en": "en-US-1",
    "hi": "hi_female_1",
    "ta": "ta_female_1",
    "te": "te_female_1",
    "kn": "kn_female_1",
    "ml": "ml_female_1"
}
```

---

## 📊 Example Conversation

```
🎙️ Listening for 5 seconds...
👤 You: I'm a first-year student exploring AI... I'm not sure if I should commit yet.

🤖 Agent: That makes sense. At this stage, many students are just exploring 
and trying to understand what's worth learning before committing to anything.
What made you interested in AI in the first place?

🎙️ Listening for 5 seconds...
👤 You: I'm just curious about learning practical skills, but my parents need to be involved.

🤖 Agent: Just to make sure I guide you correctly — for longer programs or paid courses, 
do you usually decide on your own, or would you involve your parents?

🎙️ Listening for 5 seconds...
👤 You: My parents would decide. I should discuss with them first.

🤖 Agent: Thanks for sharing all of that. I'll pass this information to our admissions team, 
and they can guide you further whenever you feel ready.
```

---

## 🛠️ Development

### Adding New Intents
Edit `agent/intent.py`:
```python
class Intent(Enum):
    YOUR_NEW_INTENT = auto()
```

### Adding Policy Rules
Edit `agent/policy_engine.py`:
```python
if intent == Intent.YOUR_NEW_INTENT:
    # Your logic here
    return PolicyAction.YOUR_ACTION
```

### Adding Response Templates
Edit `agent/response_template.py`:
```python
RESPONSES = {
    "your_key": "Your response text here..."
}
```

---

## 🚨 Troubleshooting

### Audio issues
```bash
# Test if audio device is working
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### API key errors
```bash
# Make sure .env is in the project root
cat .env | grep GROQ_API_KEY
cat .env | grep DEEPGRAM_API_KEY
```

### No transcription
- Check recording volume
- Verify Deepgram API key is valid
- Test: `python -c "from stt.deepgram_stt import DeepgramSTT"`

---

## 📚 API Documentation

### CourseLeadAgent
```python
agent = CourseLeadAgent(memory, policy_engine, router)
response = agent.handle_input(text)  # Process user input
```

### VoiceLeadAgent (Main)
```python
agent = VoiceLeadAgent()
asyncio.run(agent.run())  # Start event loop
```

### DeepgramSTT
```python
stt = DeepgramSTT()
text, result = await stt.transcribe_audio(audio_np)
```

---

## 📄 License

Proprietary - Internal Use Only

---

## 💬 Support

For issues or questions, contact the development team.
