#! /usr/bin/bash

#Update to latest version of main
git fetch origin --tags $1 

#Pull changes from tag
git pull 

#Remove first docker containers
docker-compose down

#Build docker containers
docker-compose build

#LAunch docker containers
docker-compose up -d

#Run the cron file initalizer
python3 init_cron.py

#Remove existing cron file
crontab -r
#Initialize new cronfile
crontab ./flare.cron