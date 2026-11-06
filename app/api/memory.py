from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db, MemoryModel
from app.llm.rag import store_memory

router = APIRouter()

class MemoryResponse(BaseModel):
    id: int
    session_id: str
    content: str
    category: str
    importance: int

    class Config:
        from_attributes = True

class MemoryCreate(BaseModel):
    session_id: str
    content: str

@router.post("/add", response_model=dict)
def add_memory(memory: MemoryCreate):
    """Manually add a memory to the system (bypasses extractor rules)."""
    store_memory(memory.session_id, memory.content)
    return {"status": "Memory processed"}

@router.get("/all", response_model=List[MemoryResponse])
def get_all_memories(session_id: str, db: Session = Depends(get_db)):
    """Retrieve all explicit memories for a session."""
    memories = db.query(MemoryModel).filter(MemoryModel.session_id == session_id).all()
    return memories

@router.delete("/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    """Delete a memory from SQLite (Warning: Doesn't delete from ChromaDB yet)."""
    memory = db.query(MemoryModel).filter(MemoryModel.id == memory_id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    db.delete(memory)
    db.commit()
    return {"status": "Deleted"}
