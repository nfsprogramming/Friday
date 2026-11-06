import cv2
import numpy as np
import pyautogui
import os
from app.core.logger import logger

class DesktopVision:
    @staticmethod
    def find_image_on_screen(template_path: str, threshold: float = 0.8):
        """
        Uses OpenCV template matching to find an image (button, icon) on the screen.
        Returns the center coordinates (x, y) if found, else None.
        """
        if not os.path.exists(template_path):
            logger.error(f"[Vision] Template image not found: {template_path}")
            return None

        # Take a screenshot
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)
        
        # Convert RGB to BGR for OpenCV
        screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
        screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
        
        # Load template
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            logger.error(f"[Vision] Failed to load template: {template_path}")
            return None
            
        w, h = template.shape[::-1]
        
        # Perform matching
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            # Calculate center
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            logger.info(f"[Vision] Found template '{template_path}' at ({center_x}, {center_y}) with confidence {max_val:.2f}")
            return (center_x, center_y)
            
        logger.info(f"[Vision] Template '{template_path}' not found (max confidence: {max_val:.2f})")
        return None
