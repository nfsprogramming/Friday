import psutil

class TemperatureMonitor:
    @staticmethod
    def get_stats():
        stats = {}
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return stats
                
            for name, entries in temps.items():
                for entry in entries:
                    label = entry.label or name
                    # Avoid overwriting if multiple sensors have same name but no label
                    key = label if label not in stats else f"{label}_{entries.index(entry)}"
                    stats[key] = {
                        "current": entry.current,
                        "high": entry.high,
                        "critical": entry.critical
                    }
        except Exception:
            # sensors_temperatures might not be supported on this OS
            pass
            
        return stats
