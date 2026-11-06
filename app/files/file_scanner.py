import os
from app.files.metadata_store import metadata_store
from app.files.file_classifier import FileClassifier
from app.core.logger import logger

class FileScanner:
    DEFAULT_DIRECTORIES = [
        os.path.expanduser("~\\Documents"),
        os.path.expanduser("~\\Downloads"),
        os.path.expanduser("~\\Desktop"),
        r"D:\NFS's Projects"
    ]
    
    @staticmethod
    def scan_directories(directories=None):
        directories = directories or FileScanner.DEFAULT_DIRECTORIES
        logger.info(f"[FileScanner] Starting scan on {directories}")
        
        for directory in directories:
            if not os.path.exists(directory):
                continue
                
            for root, _, files in os.walk(directory):
                # Skip hidden/system folders
                if any(part.startswith('.') for part in root.split(os.sep)):
                    continue
                    
                for file in files:
                    filepath = os.path.join(root, file)
                    
                    try:
                        stat = os.stat(filepath)
                        file_data = {
                            "name": file,
                            "path": filepath,
                            "size": stat.st_size,
                            "extension": os.path.splitext(file)[1].lower(),
                            "created": stat.st_ctime,
                            "modified": stat.st_mtime,
                            "category": FileClassifier.classify(file),
                            "hash": ""
                        }
                        metadata_store.add_or_update_file(file_data)
                    except Exception:
                        pass
        logger.info("[FileScanner] Scan complete.")
