from sys import argv
import os
import argparse
import __future__
import json
import subprocess
from datetime import datetime
import hashlib 

# Argument 
parser= argparse.ArgumentParser()
parser.add_argument( "-build", "--build", action="store_const", const=1, help="construit un fichier JSON qui contient un état des choses qu'on a demandé à surveiller")
parser.add_argument( "-check", "--check", action="store_const", const=1, help="vérifie que l'état actuel est conforme à ce qui a été stocké dans | /var/ids/db.json | ")
parser.add_argument( "-init", "--init", action="store_const", const=1, help="Commande à Lancer des la PREMIERE UTILISATION")
arg = parser.parse_args()

#FONCTION ##############################################################################

def CreateFileConf():
    if os.path.exists("/etc/ids.json"):
        return
    else:
        open("/etc/ids.json", "x")
        #Write Json Conf
        ConfJson = json.dumps(BaseDataConf)
        with open("/etc/ids.json", "w") as jsonfile:
            jsonfile.write(ConfJson)
            print("Write Succes")

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
        #Bouger de place le fichier exe



def CreateRight():
    subprocess.run(['useradd    ', '-p', 'ids', 'ids'])
    subprocess.run(['chmod', '-R', 'u+rw', '/etc/ids.json'])
    subprocess.run(['chmod', '-R', 'u+rw', '/var/ids/db.json' ])
    subprocess.run(['chmod', '-R', 'u+rw', '/var/log/ids.log' ])
    subprocess.run(['chown', '-R', 'ids:ids', '/var/log/ids.log' , '/etc/ids.json', '/var/ids/db.json'])


def IsInit() -> bool:
    if os.path.exists("/etc/ids.json"):
        return True
    else:
        return False



# Data #######################################################################################
    

BaseDataConf = {
    "file":[],
    "dir":[],
    "port":False 
}

# Function Build##############################################################################


import hashlib
import os

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

# Fonction pour construire le fichier JSON
# Fonction pour construire le fichier JSON
def Build():
    if not is_initialized():
        print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        return

    watch_paths = get_watch_paths()
    files_info = [get_file_info(file_path) for file_path in watch_paths["file"]]

    conf_file_path = "/etc/ids.json"
    with open(conf_file_path, 'r') as json_file:
        config_data = json.load(json_file)

    data = {
        "build_time": str(datetime.now()), 
        "files": files_info,       
        "directories": watch_paths["dir"],  
        "port": config_data["port"]          
    }

    db_file_path = "/var/ids/db.json"
    with open(db_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Fichier JSON créé avec succès à l'emplacement : {db_file_path}")


# Fonction pour vérifier si l'initialisation a déjà été effectuée
def is_initialized() -> bool:
    return os.path.exists("/etc/ids.json")




################################################################################################


if __name__ == '__main__':


    #Verif Quelle arguement est passé
    if arg.init == 1:
        if IsInit() == False:
            CreateFileConf()
            CreateCloneJson()
            CreateLogs()
            CreateBin()
            CreateRight()
        else:
            print("Le Init a Déja etais Utilisé")

    #Verif Quelle arguement est passé
    if arg.build == 1:
        Build()
        if IsInit() == False:
            print("ERREUR: Utililse (-init) La premiere fois")
        else:
            print("build")


    #Verif Quelle arguement est passé
    if arg.check == 1:
        if IsInit() == False:
            print("ERREUR: Utililse (-init) La premiere fois")
        else:
            print("check")



