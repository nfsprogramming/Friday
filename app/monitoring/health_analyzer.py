class HealthAnalyzer:
    @staticmethod
    def analyze(snapshot: dict) -> str:
        warnings = []
        
        cpu = snapshot.get("cpu", {})
        if cpu.get("usage_percent", 0) > 90:
            warnings.append(f"High CPU Usage: {cpu.get('usage_percent')}%")
            
        ram = snapshot.get("ram", {})
        if ram.get("usage_percent", 0) > 90:
            warnings.append(f"High RAM Usage: {ram.get('usage_percent')}%")
            
        gpu = snapshot.get("gpu", {})
        if gpu.get("has_gpu") and gpu.get("usage_percent", 0) > 90:
            warnings.append(f"High GPU Usage: {gpu.get('usage_percent')}%")
            
        temps = snapshot.get("temperatures", {})
        for sensor, data in temps.items():
            if data.get("current", 0) > 85:
                warnings.append(f"Thermal Warning ({sensor}): {data.get('current')}°C")
                
        battery = snapshot.get("battery", {})
        if battery.get("has_battery") and not battery.get("is_charging") and battery.get("percentage", 100) < 20:
            warnings.append(f"Low Battery: {battery.get('percentage')}%")
            
        if not warnings:
            return "System is completely healthy. All metrics are normal."
            
        return "System Warnings Detected:\n" + "\n".join([f"- {w}" for w in warnings])
