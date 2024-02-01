#!/bin/bash

# Création des fichiers et des dossiers nécessaires
touch /etc/ids.json
mkdir -p /var/ids
touch /var/ids/db.json
touch /var/log/ids.log
mkdir -p /var/local/bin/ids

# Configuration des permissions et des propriétaires
useradd -p ids ids
chmod -R u+rw /etc/ids.json /var/ids/db.json /var/log/ids.log
chown -R ids:ids /var/log/ids.log /etc/ids.json /var/ids/db.json