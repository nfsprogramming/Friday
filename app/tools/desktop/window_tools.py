from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.desktop.window_manager import WindowManager

class ManageWindowTool(BaseTool):
    name = "manage_window"
    description = "Manages a desktop window. Requires 'title' (keyword of the window) and 'action' ('focus', 'minimize', 'maximize', 'close')."
    
    async def execute(self, title: str = "", action: str = "focus", **kwargs) -> Dict[str, Any]:
        if not title:
            return {"success": False, "error": "title is required."}
            
        try:
            success = False
            if action == "focus":
                success = WindowManager.focus(title)
            elif action == "minimize":
                success = WindowManager.minimize(title)
            elif action == "maximize":
                success = WindowManager.maximize(title)
            elif action == "close":
                success = WindowManager.close(title)
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
            if success:
                return {"success": True, "message": f"Successfully performed '{action}' on window containing '{title}'."}
            else:
                return {"success": False, "error": f"Failed to perform '{action}' or window '{title}' not found."}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(ManageWindowTool())
