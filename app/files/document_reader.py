import os
from app.core.logger import logger

class DocumentReader:
    @staticmethod
    def read_text(filepath: str) -> str:
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            if ext == '.pdf':
                from pypdf import PdfReader
                reader = PdfReader(filepath)
                return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            elif ext in ['.docx', '.doc']:
                import docx
                doc = docx.Document(filepath)
                return "\n".join([para.text for para in doc.paragraphs])
            elif ext == '.csv':
                import pandas as pd
                df = pd.read_csv(filepath)
                return df.to_string()
            elif ext in ['.txt', '.md', '.json', '.py', '.js', '.html']:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return ""
        except Exception as e:
            logger.error(f"[DocumentReader] Error reading {filepath}: {e}")
            return ""
