import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import chromadb
from app.core.logger import logger

DB_DIR = "data"
os.makedirs(DB_DIR, exist_ok=True)

SQLITE_PATH = os.path.join(DB_DIR, "friday.db")
CHROMA_DIR = os.path.join(DB_DIR, "chroma_db")

# --- SQLAlchemy Setup ---
engine = create_engine(f"sqlite:///{SQLITE_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MemoryModel(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    content = Column(String, nullable=False)
    category = Column(String, default="fact")
    importance = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatHistoryModel(Base):
    """Raw conversation history to maintain context window across restarts."""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create all tables
Base.metadata.create_all(bind=engine)
logger.info("[Database] SQLAlchemy initialized (friday.db).")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ChromaDB Setup (Semantic Vector Memory) ---
try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    memory_collection = chroma_client.get_or_create_collection(
        name="friday_memories",
        metadata={"hnsw:space": "cosine"}
    )
    logger.info("[Database] ChromaDB initialized.")
except Exception as e:
    logger.error(f"[Database] Failed to initialize ChromaDB: {e}")
    memory_collection = None
