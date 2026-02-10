"""
Conversation Memory
Stores conversation turns per session.
Compatible with agent code that expects list-like memory.
"""

class ConversationMemory:
    def __init__(self):
        self.sessions = {}
        self.current_session = None

    def start_session(self, session_id: str):
        self.sessions[session_id] = []
        self.current_session = session_id

    def add_message(self, role: str, text: str):
        if not self.current_session:
            raise RuntimeError("No active session")

        self.sessions[self.current_session].append({
            "role": role,
            "text": text
        })

    # ✅ CRITICAL: compatibility with agent.memory.append(...)
    def append(self, item):
        if not self.current_session:
            raise RuntimeError("No active session")

        self.sessions[self.current_session].append(item)

    def get_conversation(self):
        if not self.current_session:
            return []
        return self.sessions[self.current_session]
