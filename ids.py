import fire
import json
from datetime import datetime
import os

class Ids(object):
    @staticmethod
    def create_db_file():
        # Chemin complet pour le répertoire /var/ids
        ids_dir = "/var/ids"

        # Vérifie si le répertoire existe
        if not os.path.exists(ids_dir):
            # S'il n'existe pas, crée le répertoire
            os.makedirs(ids_dir)
            print(f"Created directory: {ids_dir}")

        # Chemin complet pour le fichier db.json
        db_file_path = os.path.join(ids_dir, "db.json")

        try:
            # Tente d'ouvrir le fichier en mode création ('x')
            with open(db_file_path, 'x') as json_file:
                # Initialise la structure de données à stocker dans db.json
                data = {"build_time": str(datetime.now()), "files": {}}

                # Écrit les données dans le fichier db.json
                json.dump(data, json_file, indent=2)

                # Enregistre dans les logs
                Ids.log(f"Build successful. Database saved to {db_file_path}")
        except FileExistsError:
            # Si le fichier existe déjà, imprime un message d'erreur
            print(f"Error: {db_file_path} already exists.")

    def check(self):
        print('Checking IDS...')

    def help(self):
        print('Helping IDS...')


if __name__ == '__main__':
  fire.Fire(Ids)