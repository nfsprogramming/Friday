from app.core.config import settings
from app.core.database import SessionLocal, ChatHistoryModel

class MemoryManager:
    """Manages the conversation context window for a single session using SQLite (SQLAlchemy)."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        
    def add_message(self, role: str, content: str):
        """Appends a message to the SQLite database."""
        db = SessionLocal()
        try:
            msg = ChatHistoryModel(session_id=self.session_id, role=role, content=content)
            db.add(msg)
            db.commit()
        finally:
            db.close()

    def get_history(self) -> list[dict]:
        """Returns the most recent chat history for context injection."""
        db = SessionLocal()
        try:
            limit = settings.max_context_messages
            # Query newest first to limit, then reverse for chronological order
            msgs = db.query(ChatHistoryModel).filter(
                ChatHistoryModel.session_id == self.session_id
            ).order_by(ChatHistoryModel.id.desc()).limit(limit).all()
            
            history = [{"role": m.role, "content": m.content} for m in reversed(msgs)]
            return history
        finally:
            db.close()
    
    def clear(self):
        """Clears the session memory from SQLite."""
        db = SessionLocal()
        try:
            db.query(ChatHistoryModel).filter(ChatHistoryModel.session_id == self.session_id).delete()
            db.commit()
        finally:
            db.close()
