#!/usr/bin/python3
#-*- coding Utf-8 -*-
 
################################################################################################
#
# Ce script Python à été créé afin d'effectuer des sauvegardes de manières automatisé et simple,
# en donnant les noms des fichiers à sauvegarder, les noms des archives à créer, les données 
# afin d'accéder à la base de données mysql,...). 
# Toutes ces informations sont dans un fichier variables.py de ce module python "backup".
#
# Ecrit par : Maxence Bertellin
# Date de création : 30/07/2019
# Dernière modification : 30/07/2019 
# Testé avec : Python 3
# Script Revision: 1.0
#
################################################################################################
 


# ##########
# Pour sauvegarder plusieurs bases de données en même temps, créer un fichier 
# /repertoire/dbnameslist.txt', inscriver sur chaque ligne le nom de la BDD à sauvegarder,
# puis assigner le fichier à la variable DB_NAME 
# ##########



from variables import *



######## Rotation des sauvegardes ########

# Lister les fichiers du dossier BACKUP_PATH :
os.listdir(BACKUP_PATH)
for BACKUP_FORMAT in BACKUP_LIST:
    # Si la date de BACKUP_FORMAT est plus vieille que la date DATE3 :
    if str(BACKUP_DATE) < str(DATE3):
        #os.remove(BACKUP_PATH + "/" + BACKUP_FORMAT)
        print(str(BACKUP_FORMAT)+" est plus vieille que "+ str(DATE3) + ", on supprime.")
    # Si la date de BACKUP_FORMAT est plus récente que la DATE3:
    elif str(BACKUP_DATE) > str(DATE3):
        print(str(BACKUP_FORMAT)+" est plus récente que "+ str(DATE3) + ", on conserve.")
    # Si la date de BACKUP_FORMAT est égale à DATE3:
    elif str(BACKUP_DATE) == str(DATE3):
        print("La sauvegarde du jour"+ str(DATE3) +"à déja été effectué.")



######## Contrôle de l'espace disque du poste local ########

# Vérification de l'espace disponible sur le(s) disque(s)
# Si disk_space <= 2gb
  # on arrète le script on demande de faire de la place sur le disque
# Si disk_place > 5gb
  # on continue
# Autre:
  # On print("Espace disque faible, pour cette fois ca ira, mais faites \
  # de la place pour les sauvegardes des prochains jours")
  # et on continue


######## Création de l'archive ########

# Si le chemin (repertoire) n'est pas présent:
try:
    os.stat(BACKUP_PATH)
    os.chdir(BACKUP_PATH)
except:
    os.mkdir(BACKUP_PATH)
    os.chdir(BACKUP_PATH)
# Mise en variable de l'ouverture de la création de l'archive au format ("backup.(date).tar.gz")
# Le 'w:gz' sert à comprésser l'archive .tar
BACKUP = tarfile.open(BACKUP_NAME+".tar.gz", 'w:gz')
# On ajoute les fichiers ou dossiers que l'on veut
BACKUP.add(WEBSERVER)
BACKUP.add(FILES)
# On referme l'archive
BACKUP.close()


##### Sauvegarde de la/des Base(s) de données : #####

# Vérification de l'existence du dossier de sauvegarde, si absent, il sera créé.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)
 
# Détection du nombre de BDD  à sauvegarder dans DB_NAME :
print ("Recherche de la base de données :")
# Si DB_NAME est un chemin vers un fichier
if os.path.exists(DB_NAME):
    FILE1 = open(DB_NAME)
    MULTI = 1
    # mettre 1 à la variable MULTI
    print ("Bases de données trouvées ...")
    print ("Début de la sauvegarde des bases de données de " + DB_NAME)
else:
    print ("Base de données trouvée ...")
    print ("Début de la sauvegarde de la bases de données de " + DB_NAME)
    # Sinon mettre 0
    MULTI = 0
 
# Début de la sauvegarde de la base de données :
if MULTI:
  IN_FILE = open(DB_NAME,"r")
  FLENGTH = len(IN_FILE.readlines())
  IN_FILE.close()
  P = 1
  DBFILE = open(DB_NAME,"r")
  while P <= FLENGTH:
    # lecture du nom de la BDD depuis le fichier dbfile :
    DB = DBFILE.readline()
    # Supression des lignes en trop dans le ficheir DBFILE :
    DB = DB[:-1]
    # Définition de la commande de sauvegarde MYSQL :
    DUMPCMD = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + \
    " " + DB + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + DB + ".sql"
    os.system(DUMPCMD)
    ###
    # gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + DB + ".sql"
    # os.system(gzipcmd)
    P = P + 1
    DBFILE.close()
else:
  DB = DB_NAME
  DUMPCMD = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " \
  + DB + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + DB + ".sql"
  os.system(DUMPCMD)
  ###
  # gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + DB + ".sql"
  # os.system(gzipcmd)
 
print("")
print("Sauvegarde de la base de données effectuée, dans le répertoire "+TODAYBACKUPPATH+"")


# [0] = "Lancement du script entier (vérification espace disque, sauvegarde wordpress + config serveur web  + BDD sur le poste local, sauvegarde wordpress + BDD sur le 
#        poste distant, suppression des sauvegarde de plus de X jours sur le poste local, suppression des sauvegarde de plus de X jours sur le poste distant"
# [1] = "Vérifier la place disponible sur le disque distant"
# [2] = "Effectuer une sauvegarde de wordpress + config serveur web sur le poste local"
# [3] = "Effectuer une sauvegarde de la BDD sur le poste local"
# [4] = "Supprimer des sauvegardes datant de plus de X jours sur le poste local"
# [5] = "Vérifier la place disponible sur le disque distant"
# [6] = "Effectuer une sauvegarde de wordpress + config serveur web sur le poste distant"
# [7] = "Effectuer une sauvegarde de la BDD sur le poste distant"
# [8] = "Supprimer des sauvegardes datant de plus de X jours sur le poste distant"
# [9] = ...
# [10] = Quitter le script

# time.sleep(3.5) # Faire une pause pendant 3.5s
# raw_input("Appuyer sur Entrée pour quitter")

# Faire un choix automatique (oui) au bout de 15s si besoin d'une saisie
