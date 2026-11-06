"""
Screen Vision — allows FRIDAY to see what is on the user's screen.
"""

from PIL import ImageGrab
import io
import base64

def register(mcp):

    @mcp.tool()
    async def capture_screen_base64() -> str:
        """
        Takes a screenshot of the user's primary monitor and returns it as a base64 encoded PNG string.
        Use this when you need to "look" at the screen to help the user.
        """
        try:
            # Grab screenshot
            img = ImageGrab.grab()
            
            # Save to buffer
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            
            # Encode to base64
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            return f"Failed to capture screen: {str(e)}"
