from pydantic import BaseModel, Field
from typing import Dict, Any

class IntentResult(BaseModel):
    intent: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
