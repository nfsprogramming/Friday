from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.desktop.mouse_controller import MouseController

class MoveMouseTool(BaseTool):
    name = "move_mouse"
    description = "Moves the mouse cursor to specific (x, y) coordinates on the screen."
    
    async def execute(self, x: int = 0, y: int = 0, **kwargs) -> Dict[str, Any]:
        try:
            MouseController.move(x, y)
            return {"success": True, "message": f"Moved mouse to ({x}, {y})"}
        except Exception as e:
            return {"success": False, "error": str(e)}

class ClickMouseTool(BaseTool):
    name = "click_mouse"
    description = "Clicks the mouse. Optional parameters: x, y (coordinates), button ('left', 'right', 'middle')."
    
    async def execute(self, x: int = None, y: int = None, button: str = 'left', **kwargs) -> Dict[str, Any]:
        try:
            MouseController.click(x, y, button)
            return {"success": True, "message": f"Clicked {button} mouse button."}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(MoveMouseTool())
registry.register(ClickMouseTool())
