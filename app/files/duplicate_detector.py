import hashlib
import os

class DuplicateDetector:
    @staticmethod
    def get_file_hash(filepath: str, block_size=65536) -> str:
        if not os.path.exists(filepath):
            return ""
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                buf = f.read(block_size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(block_size)
            return hasher.hexdigest()
        except Exception:
            return ""
