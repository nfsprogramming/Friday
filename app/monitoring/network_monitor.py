import psutil
import time

class NetworkMonitor:
    _last_io = None
    _last_time = None

    @staticmethod
    def get_stats():
        io = psutil.net_io_counters()
        now = time.time()
        
        stats = {
            "bytes_sent": io.bytes_sent,
            "bytes_recv": io.bytes_recv,
            "upload_speed_kbps": 0.0,
            "download_speed_kbps": 0.0
        }
        
        if NetworkMonitor._last_io and NetworkMonitor._last_time:
            time_diff = now - NetworkMonitor._last_time
            if time_diff > 0:
                sent_diff = io.bytes_sent - NetworkMonitor._last_io.bytes_sent
                recv_diff = io.bytes_recv - NetworkMonitor._last_io.bytes_recv
                
                stats["upload_speed_kbps"] = round((sent_diff / time_diff) / 1024, 2)
                stats["download_speed_kbps"] = round((recv_diff / time_diff) / 1024, 2)
                
        NetworkMonitor._last_io = io
        NetworkMonitor._last_time = now
        return stats
