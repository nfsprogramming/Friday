"""
Tool registry — imports and registers all tool modules with the MCP server.
Add new tool modules here as you build them.
"""

from friday.tools import web, system, utils, memory_tools, system_actions, screen, outlook, playwright_browser


def register_all_tools(mcp):
    """Register all tool groups onto the MCP server instance."""
    web.register(mcp)
    system.register(mcp)
    utils.register(mcp)
    memory_tools.register(mcp)
    system_actions.register(mcp)
    screen.register(mcp)
    outlook.register(mcp)
    playwright_browser.register(mcp)
