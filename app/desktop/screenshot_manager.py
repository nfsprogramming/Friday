import pyautogui
import os
from datetime import datetime
from app.core.logger import logger

class ScreenshotManager:
    @staticmethod
    def capture_screen(save_path: str = None) -> str:
        if not save_path:
            os.makedirs("data/screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"data/screenshots/screen_{timestamp}.png"
            
        logger.info(f"[Screenshot] Capturing screen to {save_path}")
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return save_path

    @staticmethod
    def capture_region(region: tuple, save_path: str = None) -> str:
        """region is (left, top, width, height)"""
        if not save_path:
            os.makedirs("data/screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"data/screenshots/region_{timestamp}.png"
            
        logger.info(f"[Screenshot] Capturing region {region} to {save_path}")
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(save_path)
        return save_path
