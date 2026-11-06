import os
import time

class DownloadsManager:
    @staticmethod
    def get_recent_downloads(limit=5):
        downloads_dir = os.path.expanduser("~\\Downloads")
        if not os.path.exists(downloads_dir):
            return []
            
        files = []
        for f in os.listdir(downloads_dir):
            filepath = os.path.join(downloads_dir, f)
            if os.path.isfile(filepath):
                files.append((f, os.path.getmtime(filepath)))
                
        files.sort(key=lambda x: x[1], reverse=True)
        return [f[0] for f in files[:limit]]
