import os
import subprocess
import logging

def setup_logger(program_name):
    RightLog()
    log_folder = '/var/log/' + program_name
    log_file = os.path.join(log_folder, 'ids_log.log')

    # Vérifie si le dossier de logs existe, sinon le crée
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Configure le logger pour écrire dans un fichier
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def RightLog():
    subprocess.run(['chmod', '-R', 'u+rw', '/var/log/ids_log.log' ])
    subprocess.run(['chown', '-R', 'ids:ids', '/var/log/ids_log.log'])
    

    