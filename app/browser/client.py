from playwright.async_api import async_playwright
import os
from app.core.logger import logger

class PlaywrightClient:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

    async def get_page(self):
        """Returns the active browser page, initializing the browser if necessary."""
        needs_reboot = False
        
        # If we already had a browser running, check if it's still alive (user might have closed it)
        if self.playwright and self.context:
            try:
                pages = self.context.pages
                if not pages:
                    self.page = await self.context.new_page()
                else:
                    self.page = pages[-1]
                # Test connection
                await self.page.title()
            except Exception:
                logger.info("[Browser] Browser was closed by user. Rebooting...")
                needs_reboot = True
                
        if not self.playwright or needs_reboot:
            if needs_reboot:
                try:
                    await self.playwright.stop()
                except:
                    pass
                    
            logger.info("[Browser] Booting Chrome engine...")
            self.playwright = await async_playwright().start()
            
            # Persistent context saves cookies & logins between restarts
            user_data_dir = os.path.join(os.getcwd(), "data", "browser_profile")
            os.makedirs(user_data_dir, exist_ok=True)
            
            # Launch Chrome in non-headless mode (visible to user)
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                channel="chrome", # Uses native Google Chrome
                args=["--start-maximized", "--disable-infobars", "--disable-blink-features=AutomationControlled"],
                ignore_default_args=["--enable-automation"],
                no_viewport=True
            )
            
            pages = self.context.pages
            if pages:
                self.page = pages[-1]
            else:
                self.page = await self.context.new_page()
                
            logger.info("[Browser] Engine started and ready.")
            
        return self.page

browser_client = PlaywrightClient()
