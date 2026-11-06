import os

class FileClassifier:
    CATEGORIES = {
        "code": [".py", ".js", ".ts", ".rs", ".java", ".c", ".cpp", ".go", ".html", ".css"],
        "document": [".pdf", ".docx", ".doc", ".txt", ".md", ".rtf"],
        "media": [".mp4", ".jpg", ".jpeg", ".png", ".gif", ".mp3", ".wav", ".mkv"],
        "archive": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "dataset": [".csv", ".xlsx", ".xls", ".json", ".xml", ".sql"]
    }
    
    @staticmethod
    def classify(filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        for category, extensions in FileClassifier.CATEGORIES.items():
            if ext in extensions:
                return category
        return "other"
