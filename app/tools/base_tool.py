from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    name: str
    description: str
    requires_confirmation: bool = False

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool and return a result dictionary."""
        pass
