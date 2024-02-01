from sys import argv
import os
import argparse
import subprocess
from datetime import datetime
import hashlib
import json

# Argument 
parser = argparse.ArgumentParser()
parser.add_argument("-build", "--build", action="store_const", const=1, help="construit un fichier JSON qui contient un état des choses qu'on a demandé à surveiller")
parser.add_argument("-check", "--check", action="store_const", const=1, help="vérifie que l'état actuel est conforme à ce qui a été stocké dans /var/ids/db.json")
parser.add_argument("-init", "--init", action="store_const", const=1, help="Commande à Lancer dès la PREMIÈRE UTILISATION")
arg = parser.parse_args()


BaseDataConf = {
    "file": [],
    "dir": [],
    "port": False
}


def create_init_script():
    script_content = """
    #!/bin/bash
    # Contenu du script d'initialisation
    """
    script_path = "/home/baptiste/IDS_Project/init_script.sh"
    with open(script_path, "w") as file:
        file.write(script_content)

    # Changer les permissions du script pour le rendre exécutable
    subprocess.run(['chmod', 'u+x', script_path])

def InitializeSystem():
    script_path = "/home/baptiste/IDS_Project/init_script.sh"
    subprocess.run([script_path])



# Fonction pour construire le fichier JSON
def Build():
    """
    Construit le fichier JSON contenant les informations de surveillance.
    """
    if not IsInitialized():
        print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        return

    watch_paths = get_watch_paths()
    files_info = [get_file_info(file_path) for file_path in watch_paths["file"]]

    data = {
        "build_time": str(datetime.now()), 
        "files": files_info,       
        "directories": watch_paths["dir"],  
        "port": BaseDataConf["port"]       
    }

    db_file_path = "/var/ids/db.json"
    with open(db_file_path, 'w') as json_file:
        json.dump(data, json_file, separators=(',', ':'))

    print(f"Fichier JSON créé avec succès à l'emplacement : {db_file_path}")

# Fonction pour vérifier si le système est initialisé
def IsInitialized() -> bool:
    return os.path.exists("/etc/ids.json")

# Fonction pour vérifier l'état actuel par rapport au fichier de surveillance
def Check():
    """
    Vérifie que l'état actuel est conforme à ce qui a été stocké dans /var/ids/db.json.
    """
    # Ajouter le code pour vérifier l'état par rapport au fichier JSON

# Fonction pour obtenir les informations sur un fichier
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

    # Calcul des hash
    with open(file_path, 'rb') as f:
        data = f.read()
        file_info["sha512"] = hashlib.sha512(data).hexdigest()
        file_info["sha256"] = hashlib.sha256(data).hexdigest()
        file_info["md5"] = hashlib.md5(data).hexdigest()

    return file_info

# Fonction pour obtenir les chemins des fichiers à surveiller à partir du fichier /etc/ids.json
def get_watch_paths():
    watch_paths = {"file": [], "dir": []}

    conf_file_path = "/etc/ids.json"
    if os.path.exists(conf_file_path):
        with open(conf_file_path, 'r') as json_file:
            config_data = json.load(json_file)
            watch_paths["file"] = config_data.get("file", [])
            watch_paths["dir"] = config_data.get("dir", [])

    return watch_paths

# Point d'entrée du script
if __name__ == '__main__':
    # Verifier quel argument est passé
    if arg.init == 1:
        create_init_script()
        InitializeSystem()

    elif arg.build == 1:
        Build()
    elif arg.check == 1:
        Check()
