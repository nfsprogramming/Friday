import chromadb
from app.core.logger import logger
import os

class SemanticSearchEngine:
    def __init__(self):
        db_path = os.path.join(os.getcwd(), "data", "vectors.db")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        # We use ChromaDB's default embedding function which uses SentenceTransformers under the hood
        from chromadb.utils import embedding_functions
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="personal_knowledge_base",
            embedding_function=self.ef
        )

    def index_document(self, doc_id: str, text: str, metadata: dict):
        if not text or not text.strip():
            return
            
        logger.info(f"[SemanticSearch] Indexing document: {doc_id}")
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def search(self, query: str, n_results: int = 3):
        logger.info(f"[SemanticSearch] Searching for: {query}")
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

semantic_search_engine = SemanticSearchEngine()
