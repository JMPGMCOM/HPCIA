import psutil
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def monitor_application(pid, interval=5):
    """Surveille un processus Windows et log son usage CPU/mémoire."""
    try:
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        logger.error(f"Le processus avec le PID {pid} n'existe pas.")
        return

    logger.info(f"Surveillance du processus {process.name()} (PID {pid})...")

    while True:
        try:
            cpu_percent = process.cpu_percent(interval=0.1)
            mem_info = process.memory_info()
            rss_mb = mem_info.rss / 1024 / 1024  # Mémoire physique
            vms_mb = mem_info.vms / 1024 / 1024  # Mémoire virtuelle

            logger.info(
                f"PID {pid} - CPU: {cpu_percent:.1f}% | "
                f"RSS: {rss_mb:.2f} MB | VMS: {vms_mb:.2f} MB"
            )
            time.sleep(interval)
        except psutil.NoSuchProcess:
            logger.error(f"Le processus {pid} n'existe plus.")
            break
        except Exception as e:
            logger.error(f"Erreur de surveillance: {e}")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python monitor.py <PID> [interval_seconds]")
        sys.exit(1)
    pid = int(sys.argv[1])
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    monitor_application(pid, interval)
