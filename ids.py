import os
import subprocess
import logging
import argparse
import hashlib
import json
import psutil
from datetime import datetime

def setup_logger(program_name):
    log_folder = '/var/log/' + program_name
    log_file = os.path.join(log_folder, 'ids_log.log')

    # Vérifie si le dossier de logs existe, sinon le crée
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Configure le logger pour écrire dans un fichier
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def log_command_execution(command, result):
    logger.info(f"Commande exécutée: {command}")
    logger.info(f"Résultat: {result}")


# Argument 
parser = argparse.ArgumentParser()
parser.add_argument("-build", "--build", action="store_const", const=1, help="construit un fichier JSON qui contient un état des choses qu'on a demandé à surveiller")
parser.add_argument("-check", "--check", action="store_const", const=1, help="vérifie que l'état actuel est conforme à ce qui a été stocké dans /var/ids/db.json")
parser.add_argument("-init", "--init", action="store_const", const=1, help="Commande à Lancer dès la PREMIÈRE UTILISATION")
arg = parser.parse_args()

# FONCTION ##############################################################################

def CreateFileConf():
    if os.path.exists("/etc/ids.json"):
        return
    else:
        open("/etc/ids.json", "x")
        # Write Json Conf
        ConfJson = json.dumps(BaseDataConf)
        with open("/etc/ids.json", "w") as jsonfile:
            jsonfile.write(ConfJson)
            logger.info("Write Success")

def CreateCloneJson():
    if os.path.isdir("/var/ids"):
        return 
    else:
        os.mkdir("/var/ids")
        open("/var/ids/db.json", "x")

def CreateRight():
    subprocess.run(['useradd', '-p', 'ids', 'ids'])
    subprocess.run(['chmod', '-R', 'u+rw', '/etc/ids.json'])
    subprocess.run(['chmod', '-R', 'u+rw', '/var/ids/db.json' ])
    subprocess.run(['chown', '-R', 'ids:ids', '/etc/ids.json', '/var/ids/db.json'])
    

def IsInit() -> bool:
    return os.path.exists("/etc/ids.json")

# Data #######################################################################################

BaseDataConf = {
    "file": [],
    "dir": [],
    "port": False
}

# Function Build##############################################################################


# Function to get the list of listening ports
def get_listening_ports():
    # Using ss command to get the list of listening ports
    result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    output = result.stdout
    return output

# Function to build the JSON file
def Build():
    if not is_initialized():
        print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        return

    watch_paths = get_watch_paths()
    files_info = [get_file_info(file_path) for file_path in watch_paths["file"]]
    directories_info = watch_paths["dir"]

    # Vérifier si la surveillance des ports est activée
    if is_port_enabled():
        listen_ports_info = get_listen_ports_info()
    else:
        listen_ports_info = []

    data = {
        "build_time": str(datetime.now()), 
        "files": files_info,       
        "directories": directories_info,  
        "port": BaseDataConf["port"],  
        "listen_ports": listen_ports_info  
    }

    db_file_path = "/var/ids/db.json"
    with open(db_file_path, 'w') as json_file:
        json.dump(data, json_file, separators=(',', ':'))

    print(f"Fichier JSON créé avec succès à l'emplacement : {db_file_path}")



def get_listen_ports_info():
    listen_ports_info = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_LISTEN:
            listen_ports_info.append({"port_number": conn.laddr.port, "protocol": conn.type})
    return listen_ports_info

def is_port_enabled():
    conf_file_path = "/etc/ids.json"
    if os.path.exists(conf_file_path):
        with open(conf_file_path, 'r') as json_file:
            config_data = json.load(json_file)
            return config_data.get("port", False)  # Renvoie la valeur de port ou False si elle n'est pas définie
    else:
        return False  # Si le fichier de configuration n'existe pas, retourne False par défaut

if __name__ == '__main__':
    # Vérifie si la surveillance des ports est activée dans le fichier de configuration
    if is_port_enabled():
        print("La surveillance des ports est activée.")
        # Ajoutez ici le code pour récupérer les informations sur les ports
    else:
        print("La surveillance des ports n'est pas activée dans le fichier de configuration.")

# Function to check if the system is initialized
def is_initialized() -> bool:
    return os.path.exists("/etc/ids.json")



# Function to get file information
def get_file_info(file_path):
    file_info = {
        "file_path": file_path,
        "sha512": None,
        "sha256": None,
        "md5": None,
        "last_modified": os.path.getmtime(file_path),
        "creation_time": os.path.getctime(file_path),
        "owner": os.stat(file_path).st_uid,
        "group": os.stat(file_path).st_gid,
        "size": os.path.getsize(file_path)
    }

    # Calculate hashes
    with open(file_path, 'rb') as f:
        data = f.read()
        file_info["sha512"] = hashlib.sha512(data).hexdigest()
        file_info["sha256"] = hashlib.sha256(data).hexdigest()
        file_info["md5"] = hashlib.md5(data).hexdigest()

    return file_info

# Function to get the paths of files to monitor from the /etc/ids.json file
def get_watch_paths():
    watch_paths = {"file": [], "dir": []}

    conf_file_path = "/etc/ids.json"
    if os.path.exists(conf_file_path):
        with open(conf_file_path, 'r') as json_file:
            config_data = json.load(json_file)
            watch_paths["file"] = config_data.get("file", [])
            watch_paths["dir"] = config_data.get("dir", [])

    return watch_paths


# Function to check if the current state is consistent with the stored state
def check_files(stored_files):
    files_changed = []

    for file_info in stored_files:
        file_path = file_info["file_path"]
        if not os.path.exists(file_path):
            files_changed.append({"file_path": file_path, "status": "missing"})
        else:
            current_last_modified = os.path.getmtime(file_path)
            stored_last_modified = file_info["last_modified"]
            if current_last_modified != stored_last_modified:
                files_changed.append({"file_path": file_path, "status": "modified"})

    return files_changed

def check_directories(stored_directories):
    directories_changed = []

    for directory in stored_directories:
        if not os.path.exists(directory):
            directories_changed.append({"directory": directory, "status": "missing"})

    return directories_changed

def generate_report(files_changed, directories_changed):
    report = {}
    if len(files_changed) > 0 or len(directories_changed) > 0:
        report["state"] = "divergent"
        report["files_changed"] = files_changed
        report["directories_changed"] = directories_changed
    else:
        report["state"] = "ok"

    return report


def Check():
    # Chargement de l'état actuel depuis le fichier db.json
    with open('/var/ids/db.json', 'r') as db_file:
        stored_state = json.load(db_file)

    # Vérification des fichiers
    files_changed = check_files(stored_state["files"])

    # Vérification des répertoires
    directories_changed = check_directories(stored_state["directories"])

    # Construction du rapport
    report = generate_report(files_changed, directories_changed)

    return report


# Main entry point of the script
if __name__ == '__main__':
    # Configure le logger
    setup_logger("IDS_Project")
    logger = logging.getLogger("IDS_Project")

    # Check which argument is passed
    if arg.init == 1:
        logger.info("Initialisation du système")
        if not IsInit():
            CreateFileConf()
            CreateCloneJson()
            CreateRight()
        else:
            print("L'initialisation a déjà été effectuée")

    if arg.build == 1:
        Build()
        logger.info("Fichier JSON construit")
        if not IsInit():
            print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        else:
            print("Construction du fichier JSON")

    if arg.check == 1:
        result = Check()
        logger.info("Rapport de vérification: " + json.dumps(result, separators=(',', ':')))
        print(json.dumps(result, separators=(',', ':')))
        if not IsInit():
            print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        else:
            print("Vérification de l'état actuel")
