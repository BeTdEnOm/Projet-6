
# Sauvegarder un site et sa configuration automatiquement


Ce script est sous licence GNU GENERAL PUBLIC LICENSE (version 3, 29 juin 2007) et sous licence
CeCILL (version 2.1, 21 juin 2013)


Ce script Python à été créé afin d'effectuer des sauvegardes de manières automatisé et simple, 
d'un site web (configuration du serveur web et contenu du site), et de sa base de données ; 
en rentrant les noms des variables dans le fichier variables.py ... 

Ce fichier ne doit être accessible en droit que pour le créateur/modificateur dudit fichier, 
et pour le script, car celui-ci contient les informations de connexion à MYSQL.


Pour l'utiliser, remplissez le fichier variables.py avec vos propres variables, puis éxecuter 
le script.

Pour une utilisation manuelle, mettez vous dans le dossier du script puis : ./save_script.py 

Pour une utilisation automatisée, ajouter une tâche Cron (crontab -e), exemple: 

Pour que le script s'éxecute tous les jours à 03h20 :

=> 20 03 * * * root save_script.py

Vous pouvez également ajouter un fichier de log à votre tâche Cron, vous donnant ainsi accès à
ce que le script renvoie dans le terminal :

=> 20 03 * * * root save_script.py &>> /var/log/save-script.log



Ecrit par : Maxence Bertellin

Date de création : 30/07/2019

Dernière modification : 13/08/2019 

Testé avec : Python 3

Script Revision: 1.0
