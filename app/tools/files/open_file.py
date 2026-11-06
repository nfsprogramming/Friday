import os
import subprocess
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry

class OpenFileTool(BaseTool):
    name = "open_file"
    description = "CRITICAL TOOL: USE THIS EXCLUSIVELY when the user asks to 'open' a file, dataset, or document. Opens the file on the desktop and returns a preview. Requires 'filepath' parameter."
    
    async def execute(self, filepath: str = "", **kwargs) -> Dict[str, Any]:
        if not filepath:
            return {"success": False, "error": "filepath parameter is required."}
            
        if filepath.lower() == "all":
            import json
            try:
                with open("data/last_search.json", "r") as f:
                    paths = json.load(f)
                if not paths:
                    return {"success": False, "error": "No files found from previous search."}
                
                opened_count = 0
                for p in paths:
                    if os.path.exists(p):
                        os.startfile(p)
                        opened_count += 1
                return {"success": True, "message": f"Successfully opened {opened_count} files from the previous search."}
            except Exception as e:
                return {"success": False, "error": f"Failed to open all files: {str(e)}"}
                
        if not os.path.exists(filepath):
            # Fallback: search the database for its full path
            import sqlite3
            try:
                conn = sqlite3.connect("data/files.db")
                cursor = conn.cursor()
                # Use LIKE to match the filename exactly, ignoring case or path
                basename = os.path.basename(filepath)
                cursor.execute('SELECT file_path FROM files WHERE file_name LIKE ? LIMIT 1', (f"%{basename}%",))
                row = cursor.fetchone()
                conn.close()
                if row:
                    filepath = row[0]
                else:
                    return {"success": False, "error": f"File not found: {filepath}"}
            except Exception as e:
                return {"success": False, "error": f"Failed to search for file: {str(e)}"}
            
        try:
            # Open file with default application on Windows
            os.startfile(filepath)
            
            # Try to read a preview to send back to the LLM so it doesn't hallucinate
            preview = ""
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    preview = f.read(1000)
            except Exception:
                preview = "[Binary or unreadable file content]"
                
            return {
                "success": True, 
                "message": f"Successfully opened file. Preview of contents:\n{preview}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(OpenFileTool())
