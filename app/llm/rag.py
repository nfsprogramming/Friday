import time
import hashlib
from datetime import datetime
from app.core.database import memory_collection, SessionLocal, MemoryModel
from app.llm.extractor import categorize_memory
from app.core.logger import logger

def generate_id(text: str) -> str:
    """Generates a unique ID based on the text hash."""
    return hashlib.md5(text.lower().encode()).hexdigest()

def store_memory(session_id: str, text: str):
    """
    Evaluates, embeds, and stores a memory if it passes the extractor rules.
    Also handles duplicate detection by checking existing vectors.
    """
    if memory_collection is None:
        return
        
    category, importance = categorize_memory(text)
    
    # Check for duplicates in ChromaDB
    try:
        results = memory_collection.query(
            query_texts=[text],
            n_results=1,
            where={"session_id": session_id}
        )
        
        # ChromaDB distance < 0.1 usually means identical or near-identical semantics
        if results and "distances" in results and results["distances"]:
            if len(results["distances"][0]) > 0 and results["distances"][0][0] < 0.1:
                logger.info(f"[RAG] Duplicate memory detected. Skipping insert for: '{text}'")
                
                # Update timestamp in SQLite
                existing_id = results["ids"][0][0]
                db = SessionLocal()
                try:
                    # The Chroma ID is a hash of the text. 
                    # We can use it to find the SQLite record if we stored the same ID, 
                    # but we are using auto-increment in SQLite. 
                    # For MVP, we simply skip duplicating the vector. 
                    pass
                finally:
                    db.close()
                return
    except Exception as e:
        logger.error(f"[RAG] Duplicate check failed: {e}")

    # Not a duplicate, proceed to store
    mem_id = generate_id(f"{text}_{time.time()}")
    
    # 1. Store in ChromaDB
    try:
        memory_collection.add(
            documents=[text],
            metadatas=[{"session_id": session_id, "category": category}],
            ids=[mem_id]
        )
        logger.info(f"[RAG] Memory embedded in ChromaDB: '{text}'")
    except Exception as e:
        logger.error(f"[RAG] Failed to store in ChromaDB: {e}")
        return

    # 2. Store in SQLite
    db = SessionLocal()
    try:
        new_memory = MemoryModel(
            session_id=session_id,
            content=text,
            category=category,
            importance=importance
        )
        db.add(new_memory)
        db.commit()
        logger.info(f"[RAG] Memory saved to SQLite: '{text}' (Category: {category})")
    except Exception as e:
        logger.error(f"[RAG] Failed to save memory to SQLite: {e}")
    finally:
        db.close()

def retrieve_memories(session_id: str, query: str, top_k: int = 3) -> list[str]:
    """Searches ChromaDB for memories mathematically similar to the query."""
    if memory_collection is None:
        return []
        
    try:
        results = memory_collection.query(
            query_texts=[query],
            n_results=top_k,
            where={"session_id": session_id}
        )
        
        if results and "documents" in results and results["documents"]:
            return results["documents"][0]
        return []
    except Exception as e:
        logger.error(f"[RAG] Failed to retrieve memories: {e}")
        return []
