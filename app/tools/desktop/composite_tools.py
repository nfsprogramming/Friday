from typing import Dict, Any
import time
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.desktop.application_controller import ApplicationController
from app.desktop.keyboard_controller import KeyboardController

class OpenAndTypeTool(BaseTool):
    name = "open_and_type"
    description = "Opens a desktop application and immediately types text into it. Requires 'app_name' and 'text'."
    
    async def execute(self, app_name: str = "", text: str = "", **kwargs) -> Dict[str, Any]:
        if not app_name or not text:
            return {"success": False, "error": "app_name and text are required."}
            
        try:
            # Launch the app
            app_launched = ApplicationController.launch_app(app_name)
            if not app_launched:
                return {"success": False, "error": f"Failed to launch {app_name}."}
                
            # Wait for the app to open and gain focus natively
            time.sleep(2.0)
            
            # Type the text
            KeyboardController.type_text(text)
            
            return {"success": True, "message": f"Successfully launched {app_name} and typed: {text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(OpenAndTypeTool())
