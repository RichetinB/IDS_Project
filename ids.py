import fire
import json
from datetime import datetime
import os
import subprocess

class Ids(object):

    def CreateRight():
        subprocess.run(['useradd', '-p', 'ids', 'ids'])
        subprocess.run(['chmod', '-R', 'u+rw', '/etc/ids.json'])
        subprocess.run(['chmod', '-R', 'u+rw', '/var/ids/db.json' ])
        subprocess.run(['chmod', '-R', 'u+rw', '/var/log/ids.log' ])
        subprocess.run(['chown', '-R', 'ids:ids', '/var/log/ids.log' , '/etc/ids.json', '/var/ids/db.json'])


    @staticmethod
    def build():
        Ids.CreateRight()

        ids_dir = "/var/ids"

        if not os.path.exists(ids_dir):
            os.makedirs(ids_dir)
            print(f"Created directory: {ids_dir}")

        db_file_path = os.path.join(ids_dir, "db.json")

        try:
            with open(db_file_path, 'x') as json_file:
                data = {"build_time": str(datetime.now()), "files": {}}

                json.dump(data, json_file, indent=2)

                Ids.log(f"Build successful. Database saved to {db_file_path}")
        except FileExistsError:

            print(f"Error: {db_file_path} already exists.")

    def CreateRight():
        subprocess.run(['useradd', '-p', 'ids', 'ids'])
        subprocess.run(['chmod', '-R', 'u+rw', '/etc/ids.json'])
        subprocess.run(['chmod', '-R', 'u+rw', '/var/ids/db.json' ])
        subprocess.run(['chmod', '-R', 'u+rw', '/var/log/ids.log' ])
        subprocess.run(['chown', '-R', 'ids:ids', '/var/log/ids.log' , '/etc/ids.json', '/var/ids/db.json'])

    def check(self):
        print('Checking IDS...')

    def help(self):
        print('Helping IDS...')


if __name__ == '__main__':
  fire.Fire(Ids)