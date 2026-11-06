import pygetwindow as gw
from app.core.logger import logger

class WindowManager:
    @staticmethod
    def find_window(title_keyword: str):
        windows = gw.getWindowsWithTitle(title_keyword)
        if not windows:
            return None
        return windows[0]

    @staticmethod
    def focus(title_keyword: str) -> bool:
        win = WindowManager.find_window(title_keyword)
        if win:
            logger.info(f"[Window] Focusing window: {win.title}")
            win.activate()
            return True
        logger.error(f"[Window] Window not found: {title_keyword}")
        return False

    @staticmethod
    def minimize(title_keyword: str) -> bool:
        win = WindowManager.find_window(title_keyword)
        if win:
            logger.info(f"[Window] Minimizing window: {win.title}")
            win.minimize()
            return True
        return False

    @staticmethod
    def maximize(title_keyword: str) -> bool:
        win = WindowManager.find_window(title_keyword)
        if win:
            logger.info(f"[Window] Maximizing window: {win.title}")
            win.maximize()
            return True
        return False

    @staticmethod
    def close(title_keyword: str) -> bool:
        win = WindowManager.find_window(title_keyword)
        if win:
            logger.info(f"[Window] Closing window: {win.title}")
            win.close()
            return True
        return False
