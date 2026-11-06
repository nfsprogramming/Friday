import urllib.parse
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.browser.client import browser_client

class SearchYouTubeTool(BaseTool):
    name = "search_youtube"
    description = "Searches YouTube for a video/song and opens the results. Requires parameter 'query'."
    
    async def execute(self, query: str = "", **kwargs) -> Dict[str, Any]:
        if not query:
            return {"success": False, "error": "query parameter is required."}
            
        try:
            page = await browser_client.get_page()
            safe_query = urllib.parse.quote_plus(query)
            await page.goto(f"https://www.youtube.com/results?search_query={safe_query}")
            
            # Wait for search results to load and click the first video to start playing
            try:
                await page.wait_for_selector("ytd-video-renderer a#video-title", timeout=5000)
                await page.click("ytd-video-renderer a#video-title")
                return {"success": True, "message": f"Successfully searched YouTube and started playing the first result for '{query}'."}
            except Exception as e:
                # If it times out or fails to click, we at least opened the search results
                return {"success": True, "message": f"Successfully searched YouTube for '{query}', but could not auto-play the video."}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(SearchYouTubeTool())
