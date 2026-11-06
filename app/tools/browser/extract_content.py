from bs4 import BeautifulSoup
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.browser.client import browser_client

class ExtractContentTool(BaseTool):
    name = "extract_content"
    description = "Reads and extracts the readable text content from the currently active browser tab. Use this to summarize pages."
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            page = await browser_client.get_page()
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer", "aside"]):
                script.decompose()
                
            text = soup.get_text(separator=' ', strip=True)
            # Truncate text to avoid blowing up the LLM context (e.g. max 3000 chars)
            truncated_text = text[:3000] + "..." if len(text) > 3000 else text
            
            return {"success": True, "message": f"Extracted Text:\n{truncated_text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(ExtractContentTool())
