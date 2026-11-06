from pydantic import BaseModel

class Settings(BaseModel):
    # LLM Settings
    model_name: str = "qwen2.5:7b-instruct-q4_K_M"
    ollama_base_url: str = "http://localhost:11434"
    
    # Memory Settings
    max_context_messages: int = 20
    
    # Assistant Settings
    assistant_name: str = "FRIDAY"

settings = Settings()
