import os
import psutil
import subprocess
from app.core.logger import logger

class ApplicationController:
    @staticmethod
    def launch_app(app_name: str):
        logger.info(f"[Application] Launching {app_name}")
        try:
            if os.name == 'nt':
                # Try to use os.startfile for native windows paths or known aliases
                os.startfile(app_name)
            else:
                subprocess.Popen([app_name])
            return True
        except Exception as e:
            logger.error(f"[Application] Failed to launch {app_name}: {e}")
            return False

    @staticmethod
    def close_app(process_name: str) -> bool:
        logger.info(f"[Application] Attempting to close process: {process_name}")
        killed = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return killed

    @staticmethod
    def check_status(process_name: str) -> bool:
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
