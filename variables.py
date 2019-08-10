#!/usr/bin/python3
#-*- coding Utf-8 -*-



### IMPORT ###
import time, datetime, os, glob, string, getopt, re, sys, tarfile, pipes
import os.path
from os.path import basename, splitext



### VARIABLES ###
DATE = datetime.date.today()
DATE3 = datetime.date.today()-datetime.timedelta(3)
BACKUP_PATH = '/backup'
TODAYBACKUPPATH = BACKUP_PATH + '/' + str(DATE) + "." + "mysql" 
DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = 'admin'
DB_NAME = 'wordpress'
# DB_NAME = '/backup/dbnameslist.txt'
DATE3 = datetime.date.today()-datetime.timedelta(3) 
BACKUP_NAME = "backup." + str(DATE)
WEBSERVER = "/etc/apache2"
FILES = "/var/wwww"
DATABASE_NAME = "wordpress"
BACKUP_FORMAT = 'backup.*.tar.gz'
BACKUP_DATE = BACKUP_FORMAT[7:17]
BACKUP_LIST = glob.glob('backup.*.tar.gz')