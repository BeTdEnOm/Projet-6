#!/usr/bin/python3
#-*- coding Utf-8 -*-

### IMPORT ###
import time, datetime, os, glob, string, getopt, re, sys, tarfile, pipes, shutil
import os.path
import subprocess, readline
from os.path import basename, splitext


### VARIABLES A PERSONNALISER ###
# Pour sauvegarder plusieurs bases de données en même temps, créez un fichier 
# /repertoire/dbnameslist.txt', inscrivez sur chaque ligne le nom de la BDD à sauvegarder,
# puis assignez le fichier à la variable DB_NAME 
# DB_NAME = '/backup/dbnameslist.txt'

# Nom de la BDD à sauvegarder :
DB_NAME = 'wordpress'
# Nom du poste sur lequel est la BDD :
DB_HOST = 'localhost' 
# Nom de l'utilisateur autorisé à se connecter à MYSQL :
DB_USER = 'root'
# Mot de passe de l'utilisateur autorisé à se connecter à MYSQL :
DB_USER_PASSWORD = 'admin'
# Attribue la date du jour à DATE :
DATE = datetime.date.today()
# Nom donné pour l'archive
# Si vous modifier le format du BACKUP_NAME, modifier BACKUP_DATE (script) en conséquence
BACKUP_NAME = "backup." + str(DATE)
# Fichier de configuration du serveur web :
FILE1 = "/etc/apache2"
# Fichiers contenant le/les site(s) :
FILE2 = "/var/www"
# Nom du chemin dans lequel on va copier l'archive :
BACKUP_PATH = '/backup'
# Récuperation des données espace disque sur "/" :
total, used, free = shutil.disk_usage("/")
# Espace disque minimal requis (en Mo) :
MINIMUM_SPACE_DISK_REQUIRED = 2000
