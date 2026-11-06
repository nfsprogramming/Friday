from typing import Dict, Any
from app.tools.registry import registry
from app.core.logger import logger
from app.tts.speech_queue import SpeechQueue

class ToolExecutor:
    def __init__(self, speech_q=None):
        self.speech_q = speech_q

    async def execute(self, intent: str, parameters: Dict[str, Any]) -> str:
        """Executes a tool and returns the result as a string to inject into the LLM context."""
        if intent == "chat" or intent == "none":
            return ""
            
        tool = registry.get_tool(intent)
        if not tool:
            logger.warning(f"[Executor] Unknown tool requested: {intent}")
            return f"Error: Tool '{intent}' not found."
            
        if tool.requires_confirmation:
            # We enforce a simple vocal pause if speech_q is available
            if self.speech_q:
                self.speech_q.speak(f"Sir, executing {tool.name} is considered a dangerous action. Bypassing safety protocol for demonstration.")
                self.speech_q.wait_until_done()
            else:
                logger.warning(f"[Executor] Safety bypassed for {tool.name} (no speech_q available)")
            
        logger.info(f"[Executor] Executing {tool.name} with {parameters}")
        try:
            result = await tool.execute(**parameters)
            if result.get("success"):
                return f"Tool Execution Success: {result.get('message', '')}"
            else:
                return f"Tool Execution Failed: {result.get('error', 'Unknown error')}"
        except Exception as e:
            logger.error(f"[Executor] Tool crashed: {e}")
            return f"Tool Execution Error: {e}"
