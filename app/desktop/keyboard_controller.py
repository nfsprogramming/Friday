import pyautogui
from app.core.logger import logger

class KeyboardController:
    @staticmethod
    def type_text(text: str, interval: float = 0.05):
        logger.info(f"[Keyboard] Typing text: '{text}'")
        pyautogui.write(text, interval=interval)

    @staticmethod
    def press_key(key: str):
        logger.info(f"[Keyboard] Pressing key: '{key}'")
        pyautogui.press(key)

    @staticmethod
    def hotkey(*keys):
        logger.info(f"[Keyboard] Executing hotkey: {keys}")
        pyautogui.hotkey(*keys)
