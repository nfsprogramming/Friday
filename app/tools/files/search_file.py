import os
from pathlib import Path
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry

class SearchFileTool(BaseTool):
    name = "search_file"
    description = "Searches for a specific file by name in the user's Desktop, Documents, and Downloads. Requires parameter 'filename'."
    
    async def execute(self, filename: str = "", **kwargs) -> Dict[str, Any]:
        if not filename:
            return {"success": False, "error": "filename parameter is required."}
            
        import sqlite3
        try:
            conn = sqlite3.connect("data/files.db")
            cursor = conn.cursor()
            # Use LIKE to match the filename exactly, ignoring case or path
            cursor.execute('SELECT file_name, file_path FROM files WHERE file_name LIKE ? LIMIT 5', (f"%{filename}%",))
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                import json
                try:
                    with open("data/last_search.json", "w") as f:
                        json.dump([r[1] for r in rows], f)
                except Exception:
                    pass
                results_str = "\n".join([f"{r[0]} ({r[1]})" for r in rows])
                return {"success": True, "message": f"Found {len(rows)} file(s):\n{results_str}"}
            else:
                return {"success": False, "error": f"Could not find any files matching '{filename}'."}
        except Exception as e:
            return {"success": False, "error": f"Failed to search database: {str(e)}"}

registry.register(SearchFileTool())
