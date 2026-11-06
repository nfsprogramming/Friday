import psutil
from typing import Dict, Any
from app.tools.base_tool import BaseTool
from app.tools.registry import registry

import json
from app.monitoring.telemetry_service import telemetry_service
from app.monitoring.health_analyzer import HealthAnalyzer

class SystemInfoTool(BaseTool):
    name = "system_info"
    description = "Fetches a comprehensive real-time snapshot of the system's hardware health including CPU, GPU, RAM, Disk, Network, Battery, and Temperatures. Use this to monitor system performance."
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            snapshot = telemetry_service.get_current_snapshot()
            analysis = HealthAnalyzer.analyze(snapshot)
            
            # Format a clean string response
            msg = f"--- System Snapshot ---\n"
            msg += f"CPU ({snapshot['cpu'].get('name', 'CPU')}): {snapshot['cpu'].get('usage_percent', 0)}%\n"
            msg += f"RAM ({snapshot['ram'].get('speed_mhz', 'Unknown')} MHz): {snapshot['ram'].get('usage_percent', 0)}% ({snapshot['ram'].get('free_gb', 0)}GB free)\n"
            msg += f"Disk ({snapshot['disk'].get('name', 'Disk')}): {snapshot['disk'].get('usage_percent', 0)}% used\n"
            if snapshot['gpu'].get('has_gpu'):
                msg += f"GPU ({snapshot['gpu'].get('name', 'GPU')}): {snapshot['gpu'].get('usage_percent', 0)}% (Temp: {snapshot['gpu'].get('temperature_c', 'N/A')}°C)\n"
            
            if snapshot['battery'].get('has_battery'):
                charging = "Charging" if snapshot['battery'].get('is_charging') else "Discharging"
                msg += f"Battery: {snapshot['battery'].get('percentage', 0)}% ({charging})\n"
                
            msg += f"\n--- Analysis ---\n{analysis}"
            
            return {"success": True, "message": msg}
        except Exception as e:
            return {"success": False, "error": str(e)}

registry.register(SystemInfoTool())
