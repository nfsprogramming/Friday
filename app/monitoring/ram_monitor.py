import psutil
import subprocess
import os

class RAMMonitor:
    @staticmethod
    def get_stats():
        speed_mhz = "Unknown"
        if os.name == "nt":
            try:
                out = subprocess.check_output(['powershell', '-Command', "Get-CimInstance Win32_PhysicalMemory | Select-Object -ExpandProperty Speed"]).decode().strip()
                if out: speed_mhz = out.split('\n')[0].strip() # Take the first stick's speed
            except: pass

        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "speed_mhz": speed_mhz,
            "total_gb": round(mem.total / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "free_gb": round(mem.available / (1024**3), 2),
            "usage_percent": mem.percent,
            "swap_total_gb": round(swap.total / (1024**3), 2),
            "swap_used_gb": round(swap.used / (1024**3), 2),
            "swap_percent": swap.percent
        }
