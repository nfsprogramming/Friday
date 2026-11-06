import pyautogui
from app.core.logger import logger

# Safety fallback: move mouse to a corner to abort
pyautogui.FAILSAFE = True

class MouseController:
    @staticmethod
    def move(x: int, y: int, duration: float = 0.5):
        logger.info(f"[Mouse] Moving to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=duration)

    @staticmethod
    def click(x: int = None, y: int = None, button: str = 'left'):
        if x is not None and y is not None:
            logger.info(f"[Mouse] Clicking {button} at ({x}, {y})")
            pyautogui.click(x=x, y=y, button=button)
        else:
            logger.info(f"[Mouse] Clicking {button} at current position")
            pyautogui.click(button=button)

    @staticmethod
    def double_click(x: int = None, y: int = None):
        if x is not None and y is not None:
            logger.info(f"[Mouse] Double clicking at ({x}, {y})")
            pyautogui.doubleClick(x=x, y=y)
        else:
            logger.info("[Mouse] Double clicking at current position")
            pyautogui.doubleClick()

    @staticmethod
    def drag(x: int, y: int, duration: float = 0.5):
        logger.info(f"[Mouse] Dragging to ({x}, {y})")
        pyautogui.dragTo(x, y, duration=duration)

    @staticmethod
    def scroll(clicks: int):
        logger.info(f"[Mouse] Scrolling {clicks} clicks")
        pyautogui.scroll(clicks)
