import os

class ProjectDetector:
    PROJECT_MARKERS = {
        "python": ["requirements.txt", "setup.py", "pyproject.toml"],
        "node": ["package.json"],
        "rust": ["Cargo.toml"],
        "flutter": ["pubspec.yaml"],
        "git": [".git"]
    }
    
    @staticmethod
    def detect_projects(base_dir: str):
        projects = []
        for root, dirs, files in os.walk(base_dir):
            project_type = None
            for p_type, markers in ProjectDetector.PROJECT_MARKERS.items():
                if any(marker in files or marker in dirs for marker in markers):
                    project_type = p_type
                    break
            
            if project_type:
                projects.append({
                    "name": os.path.basename(root),
                    "path": root,
                    "type": project_type
                })
                # Prevent recursing into subdirectories of an identified project
                dirs.clear()
        return projects
