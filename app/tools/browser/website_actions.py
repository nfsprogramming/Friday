from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.browser.client import browser_client

class ClickElementTool(BaseTool):
    name = "click_element"
    description = "Clicks an element on the current webpage using a CSS selector (e.g. 'button#submit', '.search-btn', 'text=\"Login\"')."
    
    async def execute(self, selector: str = "", **kwargs) -> Dict[str, Any]:
        if not selector:
            return {"success": False, "error": "selector is required."}
            
        try:
            page = await browser_client.get_page()
            await page.click(selector, timeout=5000)
            return {"success": True, "message": f"Successfully clicked '{selector}'."}
        except Exception as e:
            return {"success": False, "error": str(e)}

class FillInputTool(BaseTool):
    name = "fill_input"
    description = "Types text into an input field on the current webpage using a CSS selector (e.g. 'input#search', 'textarea[name=\"q\"]', '[placeholder=\"Search\"]')."
    
    async def execute(self, selector: str = "", text: str = "", **kwargs) -> Dict[str, Any]:
        if not selector or not text:
            return {"success": False, "error": "selector and text are required."}
            
        try:
            page = await browser_client.get_page()
            await page.fill(selector, text, timeout=5000)
            return {"success": True, "message": f"Successfully typed '{text}' into '{selector}'."}
        except Exception as e:
            return {"success": False, "error": str(e)}

class PressKeyTool(BaseTool):
    name = "press_key"
    description = "Presses a keyboard key on the current webpage (e.g. 'Enter', 'Escape', 'Tab')."
    
    async def execute(self, key: str = "", **kwargs) -> Dict[str, Any]:
        if not key:
            return {"success": False, "error": "key is required."}
            
        try:
            page = await browser_client.get_page()
            await page.keyboard.press(key)
            return {"success": True, "message": f"Successfully pressed '{key}'."}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(ClickElementTool())
registry.register(FillInputTool())
registry.register(PressKeyTool())
