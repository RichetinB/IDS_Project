from sys import argv
import os
import argparse
import subprocess
from datetime import datetime
import hashlib
import json
import psutil

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
            print("Write Success")

def CreateCloneJson():
    if os.path.isdir("/var/ids"):
        return 
    else:
        os.mkdir("/var/ids")
        open("/var/ids/db.json", "x")

def CreateLogs():
    if os.path.exists("/var/log/ids.log"):
        return
    else:
        open("/var/log/ids.log", "x")

def CreateBin():
    if os.path.isdir("/var/local/bin"):
        return
    else:
        os.mkdir("/var/local/bin")
        os.mkdir("/var/local/bin/ids")
        # Move the executable file

def CreateRight():
    subprocess.run(['useradd', '-p', 'ids', 'ids'])
    subprocess.run(['chmod', '-R', 'u+rw', '/etc/ids.json'])
    subprocess.run(['chmod', '-R', 'u+rw', '/var/ids/db.json' ])
    subprocess.run(['chmod', '-R', 'u+rw', '/var/log/ids.log' ])
    subprocess.run(['chown', '-R', 'ids:ids', '/var/log/ids.log', '/etc/ids.json', '/var/ids/db.json'])
    try:
        import psutil
    except ImportError:
        print("Installing psutil...")
        subprocess.run(['pip', 'install', 'psutil'])

def IsInit() -> bool:
    return os.path.exists("/etc/ids.json")

# Data #######################################################################################

BaseDataConf = {
    "file": [],
    "dir": [],
    "port": False,
    "listen_ports": False
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

    listen_ports_info = []  # Liste des ports en écoute

    # Vérifier si la surveillance des ports est activée
    if BaseDataConf["port"]:
        # Obtenez les informations sur les ports en écoute
        listen_ports_info = get_listen_ports_info()

    data = {
        "build_time": str(datetime.now()), 
        "files": files_info,       
        "directories": directories_info,  
        "port": BaseDataConf["port"],  # Inclure l'état de la surveillance des ports
        "listen_ports": listen_ports_info  # Inclure les informations sur les ports en écoute
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

# Main entry point of the script
if __name__ == '__main__':

    # Check which argument is passed
    if arg.init == 1:
        if not IsInit():
            CreateFileConf()
            CreateCloneJson()
            CreateLogs()
            CreateBin()
            CreateRight()
        else:
            print("L'initialisation a déjà été effectuée")

    if arg.build == 1:
        Build()
        if not IsInit():
            print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        else:
            print("Construction du fichier JSON")

    if arg.check == 1:
        if not IsInit():
            print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        else:
            print("Vérification de l'état actuel")
