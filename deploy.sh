#!/usr/bin/bash

# A script that deploys flare and initializes its cron file.

#Update to latest version of main
git fetch origin --tags $1 

#Pull changes from tag
git pull 

#Remove first docker containers
docker-compose down

#Build docker containers
docker-compose build

#Launch docker containers
docker-compose up -d

#Remove existing cron file
crontab -r

#Initialize new cronfile
crontab ./flare.cron