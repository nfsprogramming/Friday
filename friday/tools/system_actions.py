"""
System Actions — Windows-native automation tools adapted from JARVIS.
"""

import os
import subprocess
from pathlib import Path

def register(mcp):

    @mcp.tool()
    async def open_terminal(command: str = "") -> str:
        """
        Open a new Windows PowerShell terminal.
        If a command is provided, it will run that command in the new terminal.
        """
        try:
            if command:
                # Open PowerShell, run command, and stay open (-NoExit)
                cmd = f'start powershell -NoExit -Command "{command}"'
            else:
                cmd = 'start powershell'
            
            subprocess.Popen(cmd, shell=True)
            return "Terminal has been opened on your screen, sir."
        except Exception as e:
            return f"Failed to open terminal: {str(e)}"

    @mcp.tool()
    async def open_browser(url: str) -> str:
        """
        Open a specific URL in the default Windows web browser.
        """
        import webbrowser
        try:
            webbrowser.open(url)
            return f"Pulled up {url} in your browser, sir."
        except Exception as e:
            return f"Failed to open browser: {str(e)}"

    @mcp.tool()
    async def start_coding_project(project_name: str, prompt: str) -> str:
        """
        Spawn an autonomous Claude Code instance to build a software project.
        This creates a new folder on the Desktop, writes the instructions to CLAUDE.md,
        and opens a PowerShell window running claude.
        """
        try:
            desktop_path = Path.home() / "Desktop"
            project_dir = desktop_path / project_name
            project_dir.mkdir(parents=True, exist_ok=True)

            # Write instructions to CLAUDE.md so claude picks them up
            claude_md = project_dir / "CLAUDE.md"
            claude_md.write_text(f"# Task\\n\\n{prompt}\\n\\nBuild this completely. If it's a web app, make sure it works standalone.")

            # Open powershell in that directory and start claude
            # -NoExit keeps the terminal open if claude crashes or finishes
            ps_cmd = f'cd "{project_dir}"; claude'
            cmd = f'start powershell -NoExit -Command "{ps_cmd}"'
            
            subprocess.Popen(cmd, shell=True)
            return f"Claude Code has been deployed to the Desktop in folder '{project_name}'. You can monitor its progress in the newly opened terminal, sir."
        except Exception as e:
            return f"Failed to deploy Claude Code: {str(e)}"
