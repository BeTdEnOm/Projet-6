#!/usr/bin/python3
#-*- coding Utf-8 -*-
 
from variables import *


total, used, free = shutil.disk_usage("/")


######## Contrôle de l'espace disque du poste local ########
print("          ##### Contrôle de l'espace disque #####")
# Récupération, de la variable espace disque libre :
DISK_ROOT_SPACE = "%d" % (free // (2**20))
# Affichage de la quantité de stockage restant sur le disque "/" :
print("Espace libre : " + DISK_ROOT_SPACE + " Mo")
# Si l'espace disque est supérieur ou égal à 2Go :
if int(DISK_ROOT_SPACE) >= MINIMUM_SPACE_DISK_REQUIRED :
  # On continue, et on l'indique
  print("L'espace disque est suffisant pour effectuer la sauvegarde.")
# Si l'espace disque est inférieur à 2Go :
elif int(DISK_ROOT_SPACE) < MINIMUM_SPACE_DISK_REQUIRED :
  # On l'indique et on ferme le programme
  print("L'espace disque est insuffisant pour effectuer la sauvegarde ;")
  print("Laisser au moins 2 Go d'espace libre puis relancer le programme.")
  exit()
print("")
