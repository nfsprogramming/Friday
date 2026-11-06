import os
import subprocess
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry

class OpenAppTool(BaseTool):
    name = "open_app"
    description = "Opens a desktop application on Windows. Requires parameter 'app_name' (e.g. 'chrome', 'code', 'notepad')."
    
    async def execute(self, app_name: str = "", **kwargs) -> Dict[str, Any]:
        if not app_name:
            return {"success": False, "error": "app_name parameter is required."}
            
        try:
            # Some Windows apps (like Spotify or Discord) require URI schemes or exact names to launch via 'start'
            app_lower = app_name.lower().strip()
            uri_overrides = {
                "spotify": "spotify:",
                "discord": "discord:",
                "settings": "ms-settings:",
                "calculator": "calculator:",
                "youtube": "https://youtube.com" # Fallback if they say open youtube before we build the browser tool
            }
            
            target = uri_overrides.get(app_lower, app_name)
            
            # On Windows, 'start' command launches apps registered in PATH, AppPaths, or URI schemes
            subprocess.Popen(f'start {target}', shell=True)
            return {"success": True, "message": f"Successfully launched {app_name}."}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(OpenAppTool())
