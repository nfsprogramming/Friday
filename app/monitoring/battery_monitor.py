import psutil

class BatteryMonitor:
    @staticmethod
    def get_stats():
        battery = psutil.sensors_battery()
        if not battery:
            return {"has_battery": False}
            
        return {
            "has_battery": True,
            "percentage": round(battery.percent, 1),
            "is_charging": battery.power_plugged,
            "time_left_mins": round(battery.secsleft / 60, 1) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else -1
        }
