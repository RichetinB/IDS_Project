import os
import json
import hashlib
import pyinotify
import argparse
from datetime import datetime

CONFIG_FILE = '/etc/ids/ids_config.json'
DB_FILE = '/var/ids/db.json'
LOG_DIR = '/var/ids/logs'

def log(message):
    log_file = os.path.join(LOG_DIR, 'ids.log')
    with open(log_file, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def load_config():
    with open(CONFIG_FILE, 'r') as json_file:
        config = json.load(json_file)
    return config

def get_file_info(file_path):
    # Cette fonction reste inchangée
    pass

def build():
    config = load_config()
    data = {"build_time": str(datetime.now()), "files": {}}

    for path in config['files']:
        if os.path.isfile(path):
            data["files"][path] = get_file_info(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    data["files"][file_path] = get_file_info(file_path)

    with open(DB_FILE, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    log("Build successful. Database saved to /var/ids/db.json")

def monitor_changes():
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_MODIFY
    notifier = pyinotify.Notifier(wm, callback=handle_file_change)

    for path in load_config()['files']:
        wm.add_watch(path, mask, rec=True)

    log("Monitoring for file changes started. Press Ctrl+C to stop.")

    try:
        while True:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        log("Monitoring stopped.")

def handle_file_change(event):
    log(f"File {event.pathname} has been modified. Updating database.")
    build()

def main():
    parser = argparse.ArgumentParser(description="Intrusion Detection System")
    parser.add_argument("command", choices=["build", "monitor"], help="Command to execute")
    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "monitor":
        monitor_changes()

if __name__ == "__main__":
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    main()
