import psutil
import time
import logging
import sys

# Configuration du système de logs pour afficher l'heure, le niveau et le message
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def monitor_application(pid, interval=5):
    """
    Surveille un processus identifié par son PID sous Windows (fonctionne aussi sous Linux).
    Log l'utilisation CPU et la mémoire du processus à intervalles réguliers.
    """
    try:
        # Tente de récupérer le processus à partir de son PID
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        logger.error(f"Le processus avec le PID {pid} n'existe pas.")
        return

    # Log le début de la surveillance avec le nom du processus
    logger.info(f"Surveillance du processus {process.name()} (PID {pid})...")

    while True:
        try:
            # Récupère le pourcentage d'utilisation CPU du processus (sur 0.1 seconde)
            cpu_percent = process.cpu_percent(interval=0.1)
            # Récupère les informations mémoire du processus
            mem_info = process.memory_info()
            rss_mb = mem_info.rss / 1024 / 1024  # Mémoire physique utilisée (en MB)
            vms_mb = mem_info.vms / 1024 / 1024  # Mémoire virtuelle utilisée (en MB)

            # Log les informations de ressources du processus
            logger.info(
                f"PID {pid} - CPU: {cpu_percent:.1f}% | "
                f"RSS: {rss_mb:.2f} MB | VMS: {vms_mb:.2f} MB"
            )
            # Attend l'intervalle spécifié avant la prochaine mesure
            time.sleep(interval)
        except psutil.NoSuchProcess:
            # Si le processus n'existe plus, log l'erreur et arrête la surveillance
            logger.error(f"Le processus {pid} n'existe plus.")
            break
        except Exception as e:
            # Pour toute autre erreur, log l'exception et arrête la surveillance
            logger.error(f"Erreur de surveillance: {e}")
            break

if __name__ == "__main__":
    # Vérifie que l'utilisateur a fourni au moins le PID en argument
    if len(sys.argv) < 2:
        print("Usage: python monitor.py <PID> [interval_seconds]")
        sys.exit(1)
    # Récupère le PID et l'intervalle depuis la ligne de commande
    pid = int(sys.argv[1])
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    # Lance la surveillance du processus
    monitor_application(pid, interval)
