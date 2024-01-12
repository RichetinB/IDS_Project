import fire
import json
import os
from datetime import datetime


class Ids(object):
  

    @staticmethod
    def build():
        # Initialise la structure de données à stocker dans db.json
        data = {"build_time": str(datetime.now()), "files": {}}

        # Chemin complet pour le fichier db.json
        db_file_path = "/var/ids/db.json"

        # Écrit les données dans le fichier db.json
        with open(db_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        # Enregistre dans les logs
        Ids.log(f"Build successful. Database saved to {db_file_path}")

    # def check(self):
    #     print('Checking IDS...')

    # def help(self):
    #     print('Helping IDS...')


if __name__ == '__main__':
  fire.Fire(Ids)