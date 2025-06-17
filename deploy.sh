#!/usr/bin/bash

# A script that deploys flare and initializes its cron file.

# Lower active containers
docker compose down

# Fetch origin            vvvvvv - This will delete any tags that origin has deleted
git fetch origin --tags --prune --prune-tags

# Checkout correct tag
git checkout $1

#Pull changes from tag
git pull 

#Remove first docker containers
docker compose down

#Build docker containers
docker compose build

#Launch docker containers
docker compose up -d

#Remove existing cron file
crontab -r

#Initialize new cronfile
crontab ./flare.cron