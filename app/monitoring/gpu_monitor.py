import GPUtil

class GPUMonitor:
    @staticmethod
    def get_stats():
        try:
            gpus = GPUtil.getGPUs()
            if not gpus:
                return {"has_gpu": False}
                
            gpu = gpus[0]
            return {
                "has_gpu": True,
                "name": gpu.name,
                "usage_percent": round(gpu.load * 100, 1),
                "memory_total_mb": gpu.memoryTotal,
                "memory_used_mb": gpu.memoryUsed,
                "memory_free_mb": gpu.memoryFree,
                "memory_percent": round(gpu.memoryUtil * 100, 1),
                "temperature_c": gpu.temperature
            }
        except Exception:
            return {"has_gpu": False}
