import sqlite3
import os
from app.core.logger import logger

class MetadataStore:
    def __init__(self, db_path="data/files.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                file_path TEXT UNIQUE,
                size INTEGER,
                extension TEXT,
                created_date REAL,
                modified_date REAL,
                file_hash TEXT,
                category TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def add_or_update_file(self, file_data: dict):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO files (file_name, file_path, size, extension, created_date, modified_date, file_hash, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_data['name'], file_data['path'], file_data['size'], 
                file_data['extension'], file_data['created'], file_data['modified'], 
                file_data.get('hash', ''), file_data.get('category', 'unknown')
            ))
            conn.commit()
        except Exception as e:
            logger.error(f"[MetadataStore] Error storing {file_data.get('path')}: {e}")
        finally:
            if conn:
                conn.close()

    def get_all_files(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM files')
        rows = cursor.fetchall()
        conn.close()
        return rows
        
    def find_by_hash(self, file_hash: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT file_path FROM files WHERE file_hash = ?', (file_hash,))
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]
        
metadata_store = MetadataStore()
