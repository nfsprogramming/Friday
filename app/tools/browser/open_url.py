from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.browser.client import browser_client

class OpenUrlTool(BaseTool):
    name = "open_url"
    description = "Opens a specific website in the browser (e.g. 'https://youtube.com', 'https://github.com'). Always include https://"
    
    async def execute(self, url: str = "", **kwargs) -> Dict[str, Any]:
        if not url:
            return {"success": False, "error": "url parameter is required."}
            
        try:
            page = await browser_client.get_page()
            await page.goto(url)
            return {"success": True, "message": f"Successfully opened {url} in the browser."}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(OpenUrlTool())
