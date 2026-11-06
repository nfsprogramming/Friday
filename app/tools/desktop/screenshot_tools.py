from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.desktop.screenshot_manager import ScreenshotManager

class TakeScreenshotTool(BaseTool):
    name = "take_screenshot"
    description = "Takes a screenshot of the entire desktop and saves it. Returns the path."
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            path = ScreenshotManager.capture_screen()
            return {"success": True, "message": f"Screenshot saved to {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(TakeScreenshotTool())
