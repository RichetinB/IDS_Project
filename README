# IDS_Project
## IDS_Project est un outil de surveillance et de vérification d'état pour les fichiers, répertoires et ports sur un système Linux.

### Installation
Pour installer l'outil IDS_Project, suivez les étapes suivantes :

- Cloner le dépôt GitHub :

```
git clone https://github.com/RichetinB/IDS_Project.git
```

- Naviguer dans le répertoire du projet :

```
cd IDS_Project
```

- Installer les dépendances Python nécessaires :

```
sudo pip install -r requirements.txt
```

- Pour afficher l'aide et les options disponibles, exécutez la commande suivante :

```
sudo python3 ids.py --help
```

- Exemple d'utilisation simple :
```
python3 ids.py -init
Cette commande initialise le système pour la première utilisation.
```

- Configuration
```
Le fichier de configuration /etc/ids.json permet de spécifier les fichiers, répertoires et ports à surveiller. Voici un exemple de contenu de ce fichier :

json
{
    "file": ["/var/log/syslog", "/etc/passwd"],
    "dir": ["/home/user/Documents", "/var/www/html"],
    "port": true
}
Dans cet exemple, nous surveillons les fichiers /var/log/syslog et /etc/passwd, les répertoires /home/user/Documents et /var/www/html, ainsi que les ports du système.

```

- Pour construire un fichier JSON contenant l'état des éléments surveillés :

```
sudo python3 ids.py -build
```

#### Le fichié JSON ce situe dans le dossier /var/ids/db.json

- Pour vérifier que l'état actuel correspond à celui stocké dans db.json :
```
sudo python3 ids.pu -check
```

#### Cette commande renvoie en format JSON l'état actuel soit par OK soit par divergent

## Log

#### Chaque commande exécuté est stocké dans un fichié de log ce situant : /var/log/IDS_Project/ids_log.log

- Ils seront stocké sous ce format 
```
[baptiste@docker IDS_Project]$ sudo cat /var/log/IDS_Project/ids_log.log
[sudo] password for baptiste:
2024-02-11 23:45:07,036 - INFO - Initialisation du système
2024-02-11 23:45:07,036 - INFO - Write Success
2024-02-11 23:46:41,696 - INFO - Initialisation du système
2024-02-11 23:46:51,208 - INFO - Initialisation du système
2024-02-11 23:47:06,916 - INFO - Initialisation du système
2024-02-11 23:47:17,038 - INFO - Fichier JSON construit
```
