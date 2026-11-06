import json
import httpx
from typing import AsyncGenerator
from app.core.config import settings
from app.core.logger import logger

class OllamaClient:
    """Asynchronous client for communicating with the local Ollama API."""
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.model_name
        self.client = httpx.AsyncClient(timeout=120.0)

    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        """Streams the LLM response token by token."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }
        
        try:
            async with self.client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
        except Exception as e:
            logger.error(f"[OllamaClient] Stream Error: {e}")
            yield "❌ Connection to brain failed."

    async def chat_sync(self, messages: list[dict]) -> str:
        """Returns the full LLM response at once (blocking wait)."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]
        except Exception as e:
            logger.error(f"[OllamaClient] Sync Error: {e}")
            return "❌ Connection to brain failed."

    async def chat_json(self, messages: list[dict]) -> dict:
        """Returns a JSON response using Ollama's format=json mode."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "format": "json"
        }
        
        try:
            response = await self.client.post(url, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            # Ollama returns a JSON string in content
            content = data.get("message", {}).get("content", "{}").strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            return json.loads(content)
        except Exception as e:
            logger.error(f"[OllamaClient] JSON Error: {e}\nContent was: {data.get('message', {}).get('content', '')}")
            return {"intent": "chat", "parameters": {}}

ollama_client = OllamaClient()
