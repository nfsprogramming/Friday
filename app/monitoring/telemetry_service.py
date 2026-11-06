import sqlite3
import os
import json
import time
from app.monitoring.cpu_monitor import CPUMonitor
from app.monitoring.gpu_monitor import GPUMonitor
from app.monitoring.ram_monitor import RAMMonitor
from app.monitoring.disk_monitor import DiskMonitor
from app.monitoring.battery_monitor import BatteryMonitor
from app.monitoring.network_monitor import NetworkMonitor
from app.monitoring.temperature_monitor import TemperatureMonitor

class TelemetryService:
    def __init__(self, db_path="data/telemetry.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                data JSON
            )
        ''')
        conn.commit()
        conn.close()

    def get_current_snapshot(self):
        return {
            "cpu": CPUMonitor.get_stats(),
            "gpu": GPUMonitor.get_stats(),
            "ram": RAMMonitor.get_stats(),
            "disk": DiskMonitor.get_stats(),
            "battery": BatteryMonitor.get_stats(),
            "network": NetworkMonitor.get_stats(),
            "temperatures": TemperatureMonitor.get_stats()
        }

    def record_snapshot(self):
        snapshot = self.get_current_snapshot()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO telemetry (timestamp, data) VALUES (?, ?)
        ''', (time.time(), json.dumps(snapshot)))
        conn.commit()
        conn.close()
        return snapshot

telemetry_service = TelemetryService()
