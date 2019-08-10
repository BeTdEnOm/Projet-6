-*- coding:Utf-8 -*-

include variables.conf

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
raw_input("Appuyer sur Entrée pour quitter")



## Script : 
## sauvegarde sur le poste local ##
# installation des paquets nécessaire: pydf,

# dans notre dossier /Backup, on supprime les sauvegarde qui ont plus de j-3
for backup-$date in /backup/:
	do:
	if backup-$date > j-3:
	on supprime
	elif backup-$date < j-3: 
	print("Le poste local est sauvegarder jusqu'à j-3")
	else backup-$date = j-3: on  ne fait rien

# on controle l'espace disque sur le poste local

# si espace disque > 2x la taille des fichiers à sauvegarder; on continue, sinon on affiche "espace disque faible, faites de la place et recommencer"
if disk_space > $disk_place:
	print("espace disque suffisant pour la sauvegarde")
# copie des fichiers à sauvegarder dans le repertoire /temp/save-$date
# on vérifie que les fichiers sont copié correctement; si oui on continue sinon on arrete et on envoie un message d'erreur
# on créé une archive de save-$date
# on vérifie que l'archive est correct; si bonne on continue sinon on arrete et on envoie un message d'erreur
# on compresse l'archive 
# on vérifie que l'archive est toujours correct apres compression; si oui on continue sinon on arrete et on envoie un message d'erreur
# on copie l'archive compressé et renommé dans le dossier /Backup sur le poste local
# on supprime nos fichiers de /temp
## sauvegarde sur le poste distant ##
# on controle l'espace disque sur le poste distant
# si espace disque > 2x la taille des fichiers à sauvegarder; on continue, sinon on affiche "espace disque faible, faites de la place et recommencer"
# dans le dossier /Backup sur le poste distant, on supprime les sauvegarde qui ont plus de j-7
# on copie le fichier archive créé à $date +0 dans serveur-distant:/Backup
# on vérifie que les fichiers sont copié correctement; si oui on continue sinon on arrete et on envoie un message d'erreur
# -- On cré un fichier log dans lequel on récapitule le déroulement du script: emplacement du fichier log, date et l'heure de création, les fichiers copié, 
# ---- le nom du dossier créé, l'emplacement de sauvegarde sur le poste local, sur le distant, l'adresse ip et le nom du poste distant, la taille de l'archive
# on écrit sur un fichier cron le lancement du script pour la date j+1
# on fait un echo du fichier log
# on quitte le script


# tar: 	-W, vérifier l'archive une fois créée
#		-u, ajoute seulement les fichiers qui sont plus récents que leurs versions respectives archivées
#		-g, créé un journal de tous les répertoires
# zipfile pour python




echo "Sauvegarde des fichiers de configuration des sites et du serveur Wordpress"
# 
tar -cvzf $backup-place$files				# Création de l'archive
											# Vérification de la présence de l'archive
if [ -e $backup-place ]
	then
											# Vérification si archive complète ou pas
		echo "Sauvegarde créé";
	else
		echo "Problème lors de la création de l'archive";
		exit
fi
echo "Sauvegarde de la BdD MySQL du serveur Wordpress"


											# copie de l'archive sur le serveur distant :
scp root@$ip-save:$backup-place$save-place
											# Vérification que l'archive soit bien copié et complète sur le serveur de sauvegarde :
if [ -e $sv-save$backup ]
	then
		echo "L’archive à bien été sauvegarder sur le serveur de sauvegarde";
	else
		echo "Problème lors de la sauvegarde sur le serveur de sauvegarde";
fi
rm $backup-place							# Suppression de l'archive sur le serveur-web
											# Suppression en fonction de la date (garder 2-3 jours de sauvegarde sur le serveur-web)
											# Suppression en fonction de la date (garder 1 semaine de sauvegarde sur le serveur-sauvegarde)


## Création d'un log dans lequel on indique : la date de la sauvegarde, les fichiers sauvegarder, et la réussite ou non de la sauvegarde (si problème ecrire là)


# mysql=sauvegarde de la base de données