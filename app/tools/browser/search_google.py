import urllib.parse
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.browser.client import browser_client

class SearchGoogleTool(BaseTool):
    name = "search_google"
    description = "Searches Google for a specific query and opens the results in the browser. Requires parameter 'query'."
    
    async def execute(self, query: str = "", **kwargs) -> Dict[str, Any]:
        if not query:
            return {"success": False, "error": "query parameter is required."}
            
        try:
            page = await browser_client.get_page()
            safe_query = urllib.parse.quote_plus(query)
            await page.goto(f"https://www.google.com/search?q={safe_query}")
            return {"success": True, "message": f"Successfully searched Google for '{query}'."}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(SearchGoogleTool())
