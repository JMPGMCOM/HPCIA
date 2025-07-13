import psutil
import time

def monitor_resources():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return {
        'cpu': cpu,
        'memory': memory,
        'disk': disk,
        'timestamp': time.time()
    }
print(monitor_resources())