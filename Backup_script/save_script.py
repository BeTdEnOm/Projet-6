#!/usr/bin/python3
#-*- coding Utf-8 -*-
 
# ###############################################################################################
#
#
# Ce script Python à été créé afin d'effectuer des sauvegardes de manières automatisé et simple, 
# d'un site web (configuration du serveur web et contenu du site), et de sa base de données ; 
# en rentrant les noms des variables dans le fichier variables.py ... 
# Ce fichier ne doit être accessible en droit que pour le créateur/modificateur dudit fichier, 
# et pour le script, car celui-ci contient les informations de connexion à MYSQL.
#
#
# Ecrit par : Maxence Bertellin
# Date de création : 30/07/2019
# Dernière modification : 12/08/2019 
# Testé avec : Python 3
# Script Revision: 0.9
#
# ###############################################################################################
#
# Pour une utilisation manuelle : ./save_script.py 
# 
# Pour une utilisation automatisée, ajouter une tâche Cron : 
#
# 20 03 * * * root save_script.py
#
# ###############################################################################################



from variables import *


print("########## Début du script de sauvegarde ##########")
print("")

######## Rotation des sauvegardes ########
print("          ##### Rotation des sauvegardes #####")
# Lister les fichiers du dossier BACKUP_PATH :
FOLDER = os.listdir(BACKUP_PATH)
# Attribue la date J-3 à DATE3 :
DATE3 = datetime.date.today()-datetime.timedelta(3)
# Pour X dans la liste FOLDER :
for X in FOLDER:
  # attribution d'un motif à BACKUP_LIST
  BACKUP_LIST = re.compile("backup.\d{4}-\d{2}-\d{2}.tar.gz")
  # Si le motif BACKUP_LIST correspond à des fichiers de X :
  if BACKUP_LIST.match(X) :
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


######## Contrôle de l'espace disque du poste local ########
print("          ##### Contrôle de l'espace disque #####")
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
  # On l'indique et on ferme le programme
  print("L'espace disque est insuffisant pour effectuer la sauvegarde ;")
  print("Laisser au moins " + str(MINIMUM_SPACE_DISK_REQUIRED) + " Mo d'espace libre puis relancer le programme.")
  exit()
print("")


##### Sauvegarde de la/des Base(s) de données #####
print("          ##### Sauvegarde de la/des base(s) de données #####")
# Détection du nombre de BDD  à sauvegarder dans DB_NAME :
print ("Recherche de la base de données ...")
# Si DB_NAME est un chemin vers un fichier :
if os.path.exists(DB_NAME):
    FILE1 = open(DB_NAME)
    MULTI = 1
    # mettre 1 à la variable MULTI
    print ("Bases de données trouvées ...")
    print ("Début de la sauvegarde des bases de données \"" + DB_NAME + "\" ...")
else:
    print ("Base de données trouvée ...")
    print ("Début de la sauvegarde de la bases de données \"" + DB_NAME + "\" ...")
    # Sinon mettre 0
    MULTI = 0
 
# Début de la sauvegarde de la base de données :
if MULTI:
  # Si multi est différent de 0, alors on lui demande d'analyser toutes les lignes :
  IN_FILE = open(DB_NAME,"r")
  FLENGTH = len(IN_FILE.readlines())
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
    os.system(DUMPCMD)
    P = P + 1
    DBFILE.close()
else:
  # Si il n'y a qu'une base de donnée à sauvegarder :
  DB = DB_NAME
  # Définition de la commande de MYSQL-DUMP > emplacement de sauvegarde :
  DUMPCMD = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " \
  + DB + " > " + BACKUP_PATH + "/" + DB_NAME + ".sql"
  os.system(DUMPCMD)
DB_BACKUP = DB_NAME + ".sql"
print("Sauvegarde de la base de données effectuée (" + DB_BACKUP + ").")
print("")



######## Création de l'archive ########
print("          ##### Création de l'archive de sauvegarde #####")
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
print("Fermeture du fichier d'archive compressé " +BACKUP_NAME + '.tar.gz' " .")
print("")
print("La sauvegarde de \"" + BACKUP_NAME + ".tar.gz" + "\" à été créée et a été placée \ndans le dossier /backup.")
# on supprime le fichier de sauvegarde de la BDD car celui-ci est dans l'archive :
os.remove(DB_BACKUP)
print("")


print("########## Fin du script de sauvegarde ##########")

print("")