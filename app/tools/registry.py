from typing import Dict, Type
from app.tools.base_tool import BaseTool
from app.core.logger import logger

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
        logger.info(f"[ToolRegistry] Registered tool: {tool.name}")

    def get_tool(self, name: str) -> BaseTool:
        return self._tools.get(name)

    def get_all_tool_schemas(self) -> list[dict]:
        """Returns JSON schema representations of all tools for the LLM."""
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]

registry = ToolRegistry()
