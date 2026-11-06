import psutil
import os
import subprocess

class DiskMonitor:
    @staticmethod
    def get_stats():
        # Get path for root/C: drive based on OS
        path = "C:\\" if os.name == "nt" else "/"
        name = "Unknown"
        if os.name == "nt":
            try:
                out = subprocess.check_output(['powershell', '-Command', "Get-CimInstance Win32_DiskDrive | Select-Object -ExpandProperty Model"]).decode().strip()
                if out: name = out.split('\\n')[0].strip() # Take the first disk if multiple
            except: pass
            
        try:
            usage = psutil.disk_usage(path)
            io = psutil.disk_io_counters()
            return {
                "name": name,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "usage_percent": usage.percent,
                "read_bytes": io.read_bytes if io else 0,
                "write_bytes": io.write_bytes if io else 0
            }
        except Exception:
            return {}
