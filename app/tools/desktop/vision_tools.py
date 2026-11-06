from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.desktop.desktop_vision import DesktopVision
from app.desktop.mouse_controller import MouseController
import time

class ClickVisualElementTool(BaseTool):
    name = "click_visual_element"
    description = "Searches for an image template on screen and clicks it. Requires 'template_path' (e.g. 'data/templates/save_button.png')."
    
    async def execute(self, template_path: str = "", **kwargs) -> Dict[str, Any]:
        if not template_path:
            return {"success": False, "error": "template_path is required."}
            
        coords = DesktopVision.find_image_on_screen(template_path)
        if coords:
            MouseController.move(coords[0], coords[1], duration=0.5)
            time.sleep(0.1)
            MouseController.click()
            return {"success": True, "message": f"Successfully found and clicked element matching {template_path}."}
        else:
            return {"success": False, "error": f"Could not find element matching {template_path} on screen."}

registry.register(ClickVisualElementTool())
