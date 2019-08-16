#!/usr/bin/python3
#-*- coding Utf-8 -*-

# ###############################################################################################
#
# Ce script est sous licence GNU GENERAL PUBLIC LICENSE (version 3, 29 juin 2007) et sous licence
# CeCILL (version 2.1, 21 juin 2013)
#
# ###############################################################################################
#
# Ecrit par : Maxence Bertellin
# Date de création : 30/07/2019
# Dernière modification : 13/08/2019 
# Testé avec : Python 3
# Script Revision: 1.0
#
# ###############################################################################################


### IMPORT NÉCESSAIRE AUX VARIABLES ###
import datetime, shutil, mysql.connector
from mysql.connector import Error


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
DB_USER = 'max'
# Mot de passe de l'utilisateur autorisé à se connecter à MYSQL :
DB_USER_PASSWORD = 'admin'
# Attribue la date du jour à DATE :
DATE = datetime.date.today()
# Attribue la date J-3 à DATE3 :
DATE3 = datetime.date.today()-datetime.timedelta(3)
# Nom donné pour l'archive, si vous modifier le format du BACKUP_NAME, modifier BACKUP_DATE (script) en conséquence :
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



### PAQUETS NÉCESSAIRES AU SCRIPT ###
PACKAGE = "python3-mysqldb"
PYTHON_PACKAGE = "mysql.connector-python"



### FONCTION ###

# Définition de la fonction CONNECT :
def CONNECT():
	# On essaie de se connecter à MySQL avec les infos de variables.py :
  try:
    conn = mysql.connector.connect(host=DB_HOST,database=DB_NAME,user=DB_USER,password=DB_USER_PASSWORD)
    conn.is_connected()
    conn.close()
    # Si ca fonctionne on retourne True comme résultat :
    return(True)
  # En exception, on attribut les erreurs à la variable ERROR :
  except Error as ERROR:
  	# On retourne l'erreur en question :
    return(ERROR)


