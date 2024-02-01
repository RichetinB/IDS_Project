from sys import argv
import os
import argparse
import __future__
import json
import subprocess
from datetime import datetime

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


def Build():
    if not IsInit():
        print("ERREUR: Utilisez d'abord -init pour initialiser le système.")
        return

    conf_file_path = "/etc/ids.json"

    with open(conf_file_path, 'r') as json_file:
        config_data = json.load(json_file)

    data = {
        "build_time": str(datetime.now()), 
        "files": config_data["file"],       
        "directories": config_data["dir"],  
        "port": config_data["port"]          
    }

    db_file_path = "/var/ids/db.json"

    with open(db_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Fichier JSON créé avec succès à l'emplacement : {db_file_path}")



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



