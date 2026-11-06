import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.core.logger import logger

class WorkspaceWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            logger.info(f"[FileWatcher] Modified: {event.src_path}")
            
    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"[FileWatcher] Created: {event.src_path}")

def start_watcher(paths):
    observer = Observer()
    handler = WorkspaceWatcher()
    for path in paths:
        if os.path.exists(path):
            observer.schedule(handler, path, recursive=True)
    observer.start()
    logger.info(f"[FileWatcher] Started watching {paths}")
    return observer
