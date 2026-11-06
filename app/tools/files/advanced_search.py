from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry
from app.files.semantic_search import semantic_search_engine
from app.files.project_detector import ProjectDetector
from app.files.downloads_manager import DownloadsManager
import os

class SemanticFileSearchTool(BaseTool):
    name = "semantic_file_search"
    description = "Searches for files based on the meaning of a query (e.g. 'internship dataset', 'budget report'). Requires parameter 'query'."
    
    async def execute(self, query: str = "", **kwargs) -> Dict[str, Any]:
        if not query:
            return {"success": False, "error": "query parameter is required."}
            
        results = semantic_search_engine.search(query, n_results=3)
        if not results['ids'] or not results['ids'][0]:
            return {"success": False, "error": "No semantically matching files found."}
            
        top_files = [doc_id for doc_id in results['ids'][0]]
        
        return {
            "success": True, 
            "message": f"Found {len(top_files)} matching files. Top match: {top_files[0]}. Other matches: {', '.join(top_files[1:])}"
        }

class ActiveProjectsTool(BaseTool):
    name = "list_active_projects"
    description = "Scans for and lists active software projects (Python, Node, Rust, etc.) in the user's Projects/Documents folder."
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        user_profile = os.environ.get("USERPROFILE", "")
        search_dirs = [
            os.path.join(user_profile, "Documents"),
            os.path.join(user_profile, "Desktop")
        ]
        
        all_projects = []
        for sdir in search_dirs:
            if os.path.exists(sdir):
                all_projects.extend(ProjectDetector.detect_projects(sdir))
                
        if not all_projects:
            return {"success": True, "message": "No active projects detected."}
            
        proj_list = [f"{p['name']} ({p['type']})" for p in all_projects]
        return {"success": True, "message": f"Found {len(all_projects)} projects: {', '.join(proj_list)}"}

class RecentDownloadsTool(BaseTool):
    name = "get_recent_downloads"
    description = "Retrieves a list of the most recently downloaded files."
    
    async def execute(self, limit: int = 5, **kwargs) -> Dict[str, Any]:
        recent = DownloadsManager.get_recent_downloads(limit)
        if not recent:
            return {"success": True, "message": "No recent downloads found."}
        return {"success": True, "message": f"Recent downloads: {', '.join(recent)}"}

registry.register(SemanticFileSearchTool())
registry.register(ActiveProjectsTool())
registry.register(RecentDownloadsTool())
