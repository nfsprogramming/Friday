from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.desktop.keyboard_controller import KeyboardController

from app.desktop.window_manager import WindowManager
import time

class TypeTextTool(BaseTool):
    name = "type_text"
    description = "Types text on the keyboard. Can optionally focus a window first if 'window_name' is provided."
    
    async def execute(self, text: str = "", window_name: str = "", **kwargs) -> Dict[str, Any]:
        if not text:
            return {"success": False, "error": "text is required."}
            
        try:
            if window_name:
                WindowManager.focus(window_name)
                time.sleep(0.5) # Give it a moment to gain focus
                
            KeyboardController.type_text(text)
            return {"success": True, "message": f"Typed text: {text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

class HotkeyTool(BaseTool):
    name = "execute_hotkey"
    description = "Executes a keyboard hotkey combination (e.g. ['ctrl', 's'], ['alt', 'f4']). Requires 'keys' (a list of strings)."
    
    async def execute(self, keys: list = None, **kwargs) -> Dict[str, Any]:
        if not keys:
            return {"success": False, "error": "keys list is required."}
        try:
            KeyboardController.hotkey(*keys)
            return {"success": True, "message": f"Executed hotkey: {'+'.join(keys)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(TypeTextTool())
registry.register(HotkeyTool())
