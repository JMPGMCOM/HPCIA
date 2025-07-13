import psutil
import time

def monitor_resources():
    # Mesure l'utilisation du CPU sur 1 seconde
    cpu = psutil.cpu_percent(interval=1)
    # Récupère le pourcentage de mémoire vive utilisée
    memory = psutil.virtual_memory().percent
    # Récupère le pourcentage d'espace disque utilisé sur la racine ('/')
    disk = psutil.disk_usage('/').percent
    # Retourne les mesures sous forme de dictionnaire, avec un timestamp (date/heure en secondes depuis l'époque Unix)
    return {
        'cpu': cpu,
        'memory': memory
