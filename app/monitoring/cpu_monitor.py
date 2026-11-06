import psutil
import subprocess
import os

class CPUMonitor:
    @staticmethod
    def get_stats():
        name = "Unknown"
        if os.name == "nt":
            try:
                out = subprocess.check_output(['powershell', '-Command', "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name"]).decode().strip()
                if out: name = out
            except: pass
            
        return {
            "name": name,
            "usage_percent": psutil.cpu_percent(interval=0.1),
            "core_count_logical": psutil.cpu_count(logical=True),
            "core_count_physical": psutil.cpu_count(logical=False),
            "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
