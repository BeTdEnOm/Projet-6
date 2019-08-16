
# Sauvegarder un site et sa configuration automatiquement


Ce script est sous licence GNU GENERAL PUBLIC LICENSE (version 3, 29 juin 2007) et sous licence
CeCILL (version 2.1, 21 juin 2013)


Ce script Python à été créé afin d'effectuer des sauvegardes de manières automatisé et simple, 
d'un site web (configuration du serveur web et contenu du site), et de sa base de données ; 
en rentrant les noms des variables dans le fichier variables.py.
Ce fichier ne doit être accessible en droit que pour le créateur/modificateur dudit fichier, 
et pour le script, car celui-ci contient les informations de connexion à MYSQL.


Pour l'utiliser, remplissez le fichier variables.py avec vos propres variables, puis exécuter 
le script.

Pour une utilisation manuelle, mettez vous dans le dossier du script puis : ./save_script.py 

Pour une utilisation automatisée, ajouter une tâche Cron (crontab -e), exemple: 

Pour que le script s'exécute tous les jours à 03h20 :

=> 20 03 * * * root save_script.py

Vous pouvez également ajouter un fichier de log à votre tâche Cron, vous donnant ainsi accès à
ce que le script renvoie dans le terminal :

=> 20 03 * * * root save_script.py &>> /var/log/save-script.log


Dans le cas ou le script ne fonctionnerait pas, vous pouvez déterminer le problème grâce à son code erreur (echo $?) :

(0) : Le script s'est déroulé sans erreur.

(1) : Le script ne s'est pas bien déroulé, mais l'erreur n'est pas répertoriée... bon courage !

(2) : L'installation du paquet de la variable PACKAGE ne s'est pas déroulé correctement.

(3) : L'installation du paquet de la variable PYTHON_PACKAGE ne s'est pas déroulé correctement.

(4) : Erreur liée au nom de la base de donnée.

(5) : Erreur liée au nom du poste à joindre (MySQL).

(6) : Erreur liée au nom d'utilisateur ou au mot de passe MySQL.

(7) : Erreur lors de l'accès à MySQL (possibilité de service offline).

(8) : Erreur lié au chemin indiqué dans la variable FILE1.

(9) : Erreur lié au chemin indiqué dans la variable FILE2.

(10) : Erreur lié à l'espace disque.

(11) : La commande de sauvegarde de BDD de MySQL ne fonctionne pas.


Ecrit par : Maxence Bertellin

Date de création : 30/07/2019

Dernière modification : 13/08/2019 

Testé avec : Python 3

Script Revision: 1.0
