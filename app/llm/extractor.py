import re

# Smarter heuristic-based extraction engine
EXTRACTION_RULES = [
    r"(?i)\bmy fav(?:orite)?\b(.*)",
    r"(?i)\bi prefer\b(.*)",
    r"(?i)\bi always\b(.*)",
    r"(?i)\b(?:i am|i'm) (?:currently )?working on\b(.*)",
    r"(?i)\bmy goal is\b(.*)",
    r"(?i)\bremember that\b(.*)",
    r"(?i)\bmy name is\b(.*)",
    r"(?i)\b(?:i am|i'm) (?:currently )?studying\b(.*)",
    r"(?i)\b(?:i am|i'm) using\b(.*)",
    r"(?i)\b(?:correction|actually|no,|update|wrong)\b(.*)"
]

def should_store_memory(text: str) -> bool:
    """
    Determines if a string is a declarative memory that should be stored.
    Filters out conversational noise.
    """
    if len(text.split()) < 2:
        return False
        
    for pattern in EXTRACTION_RULES:
        if re.search(pattern, text.strip()):
            return True
            
    return False

def categorize_memory(text: str) -> tuple[str, int]:
    """
    Returns (category, importance).
    """
    text_lower = text.lower()
    
    if "favorite" in text_lower or "fav" in text_lower or "prefer" in text_lower:
        return "preference", 8
    elif "working on" in text_lower or "project" in text_lower:
        return "project", 10
    elif "goal" in text_lower:
        return "goal", 9
    elif "name is" in text_lower or "studying" in text_lower:
        return "fact", 9
    
    return "fact", 5
