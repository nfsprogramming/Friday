import os
import sys
import psutil
import uvicorn
import asyncio
import time

# Fix Windows console emoji/unicode logging crashes
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def kill_port_8000():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # We must use 'net_connections' or similar. 
            # Psutil can be picky on Windows without admin, so let's try gracefully:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == 8000:
                    print(f"Killing old server process holding port 8000 (PID: {proc.pid})")
                    proc.kill()
                    time.sleep(1) # Give it a second to release the port
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

if __name__ == "__main__":
    kill_port_8000()
    
    if sys.platform == "win32":
        # Force the correct event loop for Playwright
        asyncio.WindowsSelectorEventLoopPolicy = asyncio.WindowsProactorEventLoopPolicy
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
    print("Starting FRIDAY API Server with ProactorEventLoop...")
    # Run uvicorn programmatically without reload to avoid event loop overwrites
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
