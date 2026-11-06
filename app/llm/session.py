from app.llm.memory import MemoryManager

class SessionManager:
    """Manages multiple chat sessions in memory."""
    def __init__(self):
        self.sessions: dict[str, MemoryManager] = {}
        
    def get_session(self, session_id: str) -> MemoryManager:
        """Retrieves or creates a memory manager for a given session ID."""
        if session_id not in self.sessions:
            self.sessions[session_id] = MemoryManager(session_id)
        return self.sessions[session_id]
        
    def delete_session(self, session_id: str):
        """Deletes a session from memory."""
        if session_id in self.sessions:
            del self.sessions[session_id]

# Global singleton for now, easily swappable to SQLite later
session_manager = SessionManager()
