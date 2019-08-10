#!/usr/bin/python3
#-*- coding Utf-8 -*-

### IMPORT ###
import time, datetime, os, glob, string, getopt, re, sys, tarfile, pipes, shutil
import os.path
import subprocess, readline
from os.path import basename, splitext


#### FONCTIONS ####
def getDfDescription():
    df = os.popen("pydf -h /")
    i = 0
    while True:
        i = i + 1
        line = df.readline()
        if i==1:
            return(line.split())
def getDf():
    df = os.popen("pydf -h /")
    i = 0
    while True:
        i = i + 1
        line = df.readline()
        if i==2:
            return(line.split())


### VARIABLES FIXE (pour le script) ###
DATE = datetime.date.today()
DATE3 = datetime.date.today()-datetime.timedelta(3)
description = getDfDescription()
disk_root = getDf()
DISK_ROOT_SPACE = int(disk_root[3][4:-1])


### VARIABLES A PERSONNALISER ###
# Pour sauvegarder plusieurs bases de données en même temps, créer un fichier 
# /repertoire/dbnameslist.txt', inscriver sur chaque ligne le nom de la BDD à sauvegarder,
# puis assigner le fichier à la variable DB_NAME 
# DB_NAME = '/backup/dbnameslist.txt'
DB_NAME = 'wordpress'
DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = 'admin'
# Si vous modifier le format du BACKUP_NAME, MODIFIER BACKUP_DATE EN CONSEQUENCE
BACKUP_NAME = "backup." + str(DATE)
FILE1 = "/etc/apache2"
FILE2 = "/var/www"
BACKUP_PATH = '/backup'
