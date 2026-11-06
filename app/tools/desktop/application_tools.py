from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.desktop.application_controller import ApplicationController

class LaunchAppTool(BaseTool):
    name = "launch_desktop_app"
    description = "Launches a desktop application by its executable name or path (e.g. 'notepad', 'calc')."
    
    async def execute(self, app_name: str = "", **kwargs) -> Dict[str, Any]:
        if not app_name:
            return {"success": False, "error": "app_name is required."}
            
        success = ApplicationController.launch_app(app_name)
        if success:
            return {"success": True, "message": f"Successfully launched {app_name}."}
        else:
            return {"success": False, "error": f"Failed to launch {app_name}."}

class CloseAppTool(BaseTool):
    name = "close_desktop_app"
    description = "Forcefully closes a desktop application process by its name (e.g. 'notepad.exe')."
    requires_confirmation = True
    
    async def execute(self, process_name: str = "", **kwargs) -> Dict[str, Any]:
        if not process_name:
            return {"success": False, "error": "process_name is required."}
            
        success = ApplicationController.close_app(process_name)
        if success:
            return {"success": True, "message": f"Successfully closed processes matching '{process_name}'."}
        else:
            return {"success": False, "error": f"No running processes found matching '{process_name}'."}

class CheckAppStatusTool(BaseTool):
    name = "check_app_status"
    description = "Checks if an application process is currently running."
    
    async def execute(self, process_name: str = "", **kwargs) -> Dict[str, Any]:
        if not process_name:
            return {"success": False, "error": "process_name is required."}
            
        is_running = ApplicationController.check_status(process_name)
        if is_running:
            return {"success": True, "message": f"Process '{process_name}' is RUNNING."}
        else:
            return {"success": True, "message": f"Process '{process_name}' is NOT running."}

registry.register(LaunchAppTool())
registry.register(CloseAppTool())
registry.register(CheckAppStatusTool())
