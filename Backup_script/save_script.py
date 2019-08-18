#!/usr/bin/python3
#-*- coding Utf-8 -*-
 
# ###############################################################################################
#
# ################### Sauvegarder un site et sa configuration automatiquement ###################
#
# ###############################################################################################
#
# Ce script est sous licence GNU GENERAL PUBLIC LICENSE (version 3, 29 juin 2007) et sous licence
# CeCILL (version 2.1, 21 juin 2013)
#
# ###############################################################################################
#
# Ce script Python à été créé afin d'effectuer des sauvegardes de manières automatisé et simple, 
# d'un site web (configuration du serveur web et contenu du site), et de sa base de données ; 
# en rentrant les noms des variables dans le fichier variables.py ... 
# Ce fichier ne doit être accessible en droit que pour le créateur/modificateur dudit fichier, 
# et pour le script, car celui-ci contient les informations de connexion à MYSQL.
#
# ###############################################################################################
#
# Pour l'utiliser, remplissez le fichier variables.py avec vos propres variables, puis exécuter 
# le script.
#
# Pour une utilisation manuelle, mettez vous dans le dossier du script puis : ./save_script.py 
# 
# Pour une utilisation automatisée, ajouter une tâche Cron (crontab -e), exemple: 
# Pour que le script s'exécute tous les jours à 03h20 :
# => 20 03 * * * /backup/save_script.py
# Vous pouvez également ajouter un fichier de log à votre tâche Cron, vous donnant ainsi accès à
# ce que le script renvoie dans le terminal, avec son code erreur en fin de log :
# => 20 03 * * * * /backup/save_script.py &>> /backup/save_script.log
#
# ###############################################################################################
#
# Dans le cas ou le script ne fonctionnerait pas, vous pouvez déterminer le problème grâce à son 
# code erreur (echo $?) :
# (0) : Le script s'est déroulé sans erreur.
# (1) : Le script ne s'est pas bien déroulé, mais l'erreur n'est pas répertoriée... bon courage !
# (2) : L'installation du paquet de la variable PACKAGE ne s'est pas déroulé correctement.
# (3) : L'installation du paquet de la variable PYTHON_PACKAGE ne s'est pas déroulé correctement.
# (4) : Erreur liée au nom de la base de donnée.
# (5) : Erreur liée au nom du poste à joindre (MySQL).
# (6) : Erreur liée au nom d'utilisateur ou au mot de passe MySQL.
# (7) : Erreur lors de l'accès à MySQL (possibilité de service offline).
# (8) : Erreur lié au chemin indiqué dans la variable FILE1.
# (9) : Erreur lié au chemin indiqué dans la variable FILE2.
# (10) : Erreur lié à l'espace disque.
# (11) : La commande de sauvegarde de BDD de MySQL ne fonctionne pas.
# (12) : Erreur lors de la création de l'archive.
#
# ###############################################################################################
#
# Ecrit par : Maxence Bertellin
# Date de création : 30/07/2019
# Dernière modification : 16/08/2019 
# Testé avec : Python 3
# Script Revision: 1.0
#
# ###############################################################################################


### IMPORT NÉCESSAIRE AU SCRIPT ###
import datetime, os, re, tarfile, shutil
import os.path
import readline
import mysql.connector
from mysql.connector import Error

from variables import *



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




print("        ########## Début du script de sauvegarde ##########")
print("")
 
######## Installation des paquets système requis pour le script ########
print("##### Installation des paquets système requis pour le script #####")

APT = "apt install "
# Si le retour de l'installation du paquet PACKAGE est égal à 0 :
if os.system(APT+PACKAGE+" -y") == 0 :
  print("Le paquet " + PACKAGE + " à été installé avec succès ou est déjà présent.")
# Si son code retour est différent de 0 :
else :
  # On indique une erreur d'installation et on quitte avec le code erreur 2.
  print("Le paquet " + PACKAGE + " est introuvable et/ou n'à pas pu être installé.")
  exit(2)

PIP = "python3 -m pip install "
# Si le retour de l'installation du paquet PACKAGE est égal à 0 :
if os.system(PIP+PYTHON_PACKAGE) == 0 :
  print("Le paquet " + PYTHON_PACKAGE + " à été installé avec succès ou est déjà présent.")
# Si son code retour est différent de 0 :
else :
  # On indique une erreur d'installation et on quitte avec le code erreur 3.
  print("Le paquet " + PYTHON_PACKAGE + " est introuvable et/ou n'à pas pu être installé.")
  exit(3)
print("")

######## Vérification des prérequis pour MySQL ########
print("##### Vérification des prérequis pour MySQL #####")
# Définition de la commande à tester :
DB = DB_NAME
DUMPCMD = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " \
+ DB + " > " + BACKUP_PATH + "/" + DB_NAME + ".sql"
# Si le retour de la commande est égal à 0 :
if os.system(DUMPCMD) == 0 :
  print("La commande de sauvegarde de BDD de MySQL fonctionne.")
  os.remove(BACKUP_PATH + "/" + DB_NAME + ".sql")
# Si son code retour est différent de 0 :
else :
  # On indique une erreur avec la commande et on quitte avec le code erreur 11.
  print("La commande de sauvegarde de BDD de MySQL ne fonctionne pas.")
  exit(11)
# Attribution du résultat de la fonction CONNECT à la variable ERROR sous forme de chaine de caractère.
ERROR = str(CONNECT())
# Si la fonction CONNECT renvoie True :
if CONNECT() is True :
  # On indique que les paramètres de connexion à MySQL sont corrects.
  print("Les paramètres de connexion à MySQL sont corrects.")
  pass
# Si ERROR == le code 1049 :
elif ERROR[0:4] == str(1049) :
  # On indique une erreur liée au nom de la base de donnée et on quitte avec le code erreur 4.
  print("Erreur " + ERROR[0:4] + " : La base de données " + DB_NAME + " dans MySQL est inconnu.")
  exit(4)
# Si ERROR == le code 2003 :
elif ERROR[0:4] == str(2003) :
  # On indique une erreur liée au nom de du poste à joindre et on quitte avec le code erreur 5.
  print("Erreur " + ERROR[0:4] + " : Impossible de joindre le poste " + DB_HOST + " dans MySQL.")
  exit(5)
# Si ERROR == le code 1045 :
elif ERROR[0:4] == str(1045) :
  # On indique une erreur liée au nom d'utilisateur ou du mot de passe et on quitte avec le code erreur 6.
  print("Erreur " + ERROR[0:4] + " : Nom d'utilisateur ou mot de passe MySQL incorrect.")
  exit(6)
else :
  # Pour toute autre type d'erreur, on l'indique puis on quitte avec le code erreur 7.
  print("Erreur lors de l'accès à MySQL.")
  exit(7)
print("")
 

######## Vérification des prérequis pour la création de la sauvegarde ########
print("##### Vérification des prérequis pour la création de la sauvegarde #####")

# On cherche à savoir si la variable FILE1 est correct :
try:
  # Si le chemin (répertoire) est présent, on change juste de répertoire pour lui ;
  os.stat(FILE1)
  print("\"" + FILE1 +"\" est un chemin valide et sera ajouté à l'archive en temps voulu.")
except:
  # On indique une erreur liée au chemin indiqué dans FILE1 et on quitte avec le code erreur 8.
  print("Le chemin \"" + FILE1 +"\" de la variable FILE1 n'existe pas.")
  exit(8)

# On cherche à savoir si la variable FILE2 est correct :
try:
  # Si le chemin (répertoire) est présent, on change juste de répertoire pour lui ;
  os.stat(FILE2)
  print("\"" + FILE2 +"\" est un chemin valide et sera ajouté à l'archive en temps voulu.")
except:
  # On indique une erreur liée au chemin indiqué dans FILE2 et on quitte avec le code erreur 9.
  print("Le chemin \"" + FILE2 +"\" de la variable FILE1 n'existe pas.")
  exit(9)
print("")


######## Contrôle de l'espace disque du poste local ########
print("##### Contrôle de l'espace disque #####")
# Récupération, de la variable espace disque libre :
DISK_ROOT_SPACE = "%d" % (free // (2**20))
# Affichage de la quantité de stockage restant sur le disque "/" :
print("Espace libre : " + DISK_ROOT_SPACE + " Mo")
# Si l'espace disque est supérieur ou égal à MINIMUM_SPACE_DISK_REQUIRED :
if int(DISK_ROOT_SPACE) >= MINIMUM_SPACE_DISK_REQUIRED :
  # On continue, et on l'indique
  print("L'espace disque est suffisant pour effectuer la sauvegarde.")
# Si l'espace disque est inférieur à MINIMUM_SPACE_DISK_REQUIRED :
elif int(DISK_ROOT_SPACE) < MINIMUM_SPACE_DISK_REQUIRED :
  # On indique une erreur liée à l'espace disque et on quitte avec le code erreur 10.
  print("L'espace disque est insuffisant pour effectuer la sauvegarde ;")
  print("Laisser au moins " + str(MINIMUM_SPACE_DISK_REQUIRED) + " Mo d'espace libre puis relancer le programme.")
  exit(10)
print("")


######## Rotation des sauvegardes ########
print("##### Rotation des sauvegardes #####")
try:
  # Si le chemin (répertoire) est présent, on change juste de répertoire pour lui ;
  os.stat(BACKUP_PATH)
  os.chdir(BACKUP_PATH)
except:
  # Si le il n'est pas présent, on le créé.
  os.mkdir(BACKUP_PATH)
  os.chdir(BACKUP_PATH)
# Lister les fichiers du dossier BACKUP_PATH :
FOLDER = os.listdir(BACKUP_PATH)
# Pour X dans la liste FOLDER :
for X in FOLDER:
  # attribution d'un motif à BACKUP_LIST
  BACKUP_LIST = re.compile("backup.\d{4}-\d{2}-\d{2}.tar.gz")
  # Si le motif BACKUP_LIST correspond à des fichiers de X :
  if BACKUP_LIST.match(X) :
    # On ne récupère que la date dans le nom du fichier :
    BACKUP_DATE = X[7:17]
    # Si la date de BACKUP_DATE est égale à DATE :
    if str(BACKUP_DATE) == str(DATE):
      print("La sauvegarde du jour "+ "(" + str(DATE) + ")" +" à déjà été effectuée.")
      exit()
    # Si le fichier est égale à J-3 :
    elif str(BACKUP_DATE) == str(DATE3):
      print(str(X) +" sera le plus vieux fichier de sauvegarde conservé.")
    # Si la date de BACKUP_DATE est plus vieille que la date J-3 :
    elif str(BACKUP_DATE) < str(DATE3):
      try :
        # On supprime le dossier
        shutil.rmtree(BACKUP_PATH + "/" + X)
      except :
        # On supprime le fichier
        os.remove(str(BACKUP_PATH) + "/" + str(X))
      print(str(X)+" est plus vieux que "+ str(DATE3) + ", on supprime.")
    # Si la date de BACKUP_DATE est plus récente que la date J-3 :
    elif str(BACKUP_DATE) > str(DATE3):
      print(str(X)+" est plus récent que "+ str(DATE3) + ", on conserve.")
print("")





##### Sauvegarde de la/des Base(s) de données #####
print("##### Sauvegarde de la/des base(s) de données #####")
# Détection du nombre de BDD  à sauvegarder dans DB_NAME :
print ("Recherche de la base de données ...")
# Si DB_NAME est un chemin vers un fichier :
if os.path.exists(DB_NAME):
    FILE1 = open(DB_NAME)
    MULTI = 1
    # mettre 1 à la variable MULTI :
    print ("Bases de données trouvées ...")
    print ("Début de la sauvegarde des bases de données \"" + DB_NAME + "\" ...")
else:
    print ("Base de données trouvée ...")
    print ("Début de la sauvegarde de la bases de données \"" + DB_NAME + "\" ...")
    # Sinon mettre 0 :
    MULTI = 0
 
# Début de la sauvegarde de la base de données :
# Si MULTI existe :
if MULTI:
  # On ouvre le fichier DB_NAME, en lecture :
  IN_FILE = open(DB_NAME,"r")
  # On lit le fichier ligne par ligne :
  FLENGTH = len(IN_FILE.readlines())
  # On ferme le fichier :
  IN_FILE.close()
  P = 1
  DBFILE = open(DB_NAME,"r")
  while P <= FLENGTH:
    # lecture du nom de la BDD depuis le fichier dbfile :
    DB = DBFILE.readline()
    # Supression des lignes en trop dans le fichier DBFILE :
    DB = DB[:-1]
    # Définition de la commande de MYSQL-DUMP > emplacement de sauvegarde :
    DUMPCMD = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + \
    " " + DB + " > " + str(BACKUP_PATH) + "/" + DB_NAME + ".sql"
    # On lance la commande DUMPCMD :
    os.system(DUMPCMD)
    # On incrémente P pour accéder à la ligne suivante :
    P = P + 1
    # On ferme le fichier DBFILE :
    DBFILE.close()
# Si MULTI n'existe pas, il n'y a qu'une BDD à sauvegarder :
else:
  # On définit DB :
  DB = DB_NAME
  # Définition de la commande de MYSQL-DUMP > emplacement de sauvegarde :
  DUMPCMD = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " \
  + DB + " > " + BACKUP_PATH + "/" + DB_NAME + ".sql"
  # On lance la commande DUMPCMD :
  os.system(DUMPCMD)
# On définit DB_BACKUP afin d'avoir le nom complet du backup :
DB_BACKUP = DB_NAME + ".sql"
print("Sauvegarde de la base de données effectuée (" + DB_BACKUP + ").")
print("")



######## Création de l'archive ########
print("##### Création de l'archive de sauvegarde #####")
try:
  # Si le chemin (répertoire) est présent, on change juste de répertoire pour lui ;
  os.stat(BACKUP_PATH)
  os.chdir(BACKUP_PATH)
except:
  # Si le il n'est pas présent, on le créé.
  os.mkdir(BACKUP_PATH)
  os.chdir(BACKUP_PATH)
print("Création et ouverture de l'archive ...")
# On créé l'archive BACKUP, le 'w:gz' sert à écrire dans l'archive tar puis à la comprésser :
with tarfile.open(BACKUP_NAME + '.tar.gz', mode='w:gz') as BACKUP :
  # On ajoute le dossier et tous le contenu de FILE1 :
  BACKUP.add(FILE1, recursive = True)
  print("Ajout du dossier" + str(FILE1) + " ...")
    # On ajoute le dossier et tous le contenu de FILE2 :
  BACKUP.add(FILE2, recursive = True)
  print("Ajout du dossier" + str(FILE2) + " ...")
  # On ajoute le fichier de sauvegarde BDD :
  BACKUP.add(DB_BACKUP)
  print("Ajout du fichier de sauvegarde de la BDD " + str(DB_BACKUP) + " ...")
# On ferme l'archive :
BACKUP.close()  
print("Fermeture du fichier d'archive compressé " +BACKUP_NAME + '.tar.gz' " .")
# on supprime le fichier de sauvegarde de la BDD car celui-ci est dans l'archive :
os.remove(DB_BACKUP)
print("")
# On lance une vérification de l'archive :
print("Vérification de l'archive ...")
# Si on peut ouvrir le fichier BACKUP_NAME.tar.gz :
try :
  # Si le fichier s'ouvre, on indique que ça c'est bien déroulé :
  BACKUP_CHECK = open(BACKUP_NAME + '.tar.gz',"r")
  print("L'archive \"" + BACKUP_NAME + ".tar.gz" + "\" à été créée et a été placée \ndans le dossier /backup.")
  # Et on referme le fichier :
  BACKUP_CHECK.close()
except :
  # Dans les autres cas, on indique qu'il y a une erreur et on quitte avec le code erreur 12 :
  print("Erreur lors de la création de l'archive.")
  exit(12)
print("")


print("########## Fin du script de sauvegarde ##########")

print("")
exit(0)