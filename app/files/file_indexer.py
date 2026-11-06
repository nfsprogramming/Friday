import os
from app.files.file_scanner import FileScanner
from app.files.metadata_store import metadata_store
from app.files.document_reader import DocumentReader
from app.files.semantic_search import semantic_search_engine
from app.core.logger import logger

class FileIndexer:
    @staticmethod
    def run_full_indexing():
        logger.info("[FileIndexer] Starting full indexing pipeline...")
        # 1. Scan files and update metadata DB
        FileScanner.scan_directories()
        
        # 2. Get all files
        all_files = metadata_store.get_all_files()
        logger.info(f"[FileIndexer] Found {len(all_files)} files to process.")
        
        # 3. Read and vector-index documents
        valid_extensions = ['.pdf', '.docx', '.txt', '.md', '.csv']
        
        for row in all_files:
            file_path = row[2]
            ext = row[4]
            
            if ext in valid_extensions and os.path.exists(file_path):
                text = DocumentReader.read_text(file_path)
                if text:
                    metadata = {
                        "file_path": file_path,
                        "file_name": row[1]
                    }
                    semantic_search_engine.index_document(file_path, text, metadata)
                    
        logger.info("[FileIndexer] Full indexing complete.")
