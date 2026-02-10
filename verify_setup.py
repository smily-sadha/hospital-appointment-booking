"""
Setup verification script
Run this to verify all dependencies and APIs are configured
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def check_environment():
    """Verify .env exists and has required keys"""
    print("✓ Checking environment setup...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("  ❌ .env file not found")
        print("     Run: cp .env.example .env")
        return False
    
    load_dotenv()
    
    required_keys = ["GROQ_API_KEY", "DEEPGRAM_API_KEY"]
    missing = []
    
    for key in required_keys:
        value = os.getenv(key)
        if not value or value.startswith("your_"):
            missing.append(key)
    
    if missing:
        print(f"  ❌ Missing API keys: {', '.join(missing)}")
        return False
    
    print("  ✅ All environment variables configured")
    return True


def check_imports():
    """Verify all required packages are installed"""
    print("\n✓ Checking dependencies...")
    
    packages = {
        "groq": "Groq LLM",
        "dotenv": "Environment variables",
        "deepgram": "Deepgram STT",
        "sounddevice": "Audio I/O",
        "numpy": "Numerical computing",
        "requests": "HTTP client",
        "pytest": "Testing framework"
    }
    
    failed = []
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} (run: pip install -r requirements.txt)")
            failed.append(module)
    
    return len(failed) == 0


def check_audio_device():
    """Verify audio device is available"""
    print("\n✓ Checking audio device...")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        # Find a default device
        default = sd.default
        print(f"  ✅ Default input device: {default.name}")
        return True
    except Exception as e:
        print(f"  ⚠️  Audio device issue: {e}")
        return True  # Non-fatal


def check_module_structure():
    """Verify project structure"""
    print("\n✓ Checking project structure...")
    
    required_files = [
        "agent/__init__.py",
        "agent/agent.py",
        "agent/policy_engine.py",
        "agent/intent.py",
        "agent/state.py",
        "stt/deepgram_stt.py",
        "llm/groq_client.py",
        "audio/recorder.py",
        "memory/memory.py",
        "main.py",
    ]
    
    failed = []
    for filepath in required_files:
        if Path(filepath).exists():
            print(f"  ✅ {filepath}")
        else:
            print(f"  ❌ {filepath} (missing)")
            failed.append(filepath)
    
    return len(failed) == 0


def check_voice_agent_imports():
    """Verify voice agent can import all components"""
    print("\n✓ Checking voice agent imports...")
    
    try:
        from agent.agent import CourseLeadAgent
        from agent.policy_engine import PolicyEngine
        from agent.router import Router
        from memory.memory import ConversationMemory
        from stt.deepgram_stt import DeepgramSTT
        from audio.recorder import record
        from audio.playback import AudioPlayer
        
        print("  ✅ All core imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("🔧 Course Lead Qualification Voice Agent - Setup Check")
    print("=" * 60 + "\n")
    
    checks = [
        ("Environment", check_environment),
        ("Dependencies", check_imports),
        ("Audio Device", check_audio_device),
        ("Project Structure", check_module_structure),
        ("Voice Agent", check_voice_agent_imports),
    ]
    
    results = []
    for name, check_fn in checks:
        try:
            result = check_fn()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} check failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_pass = all(r for _, r in results)
    
    if all_pass:
        print("\n✅ All checks passed! Run the agent with:")
        print("   python main.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
