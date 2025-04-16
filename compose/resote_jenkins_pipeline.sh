#!/bin/bash

cd /home/boris/git/stratus/compose
docker compose -f jenkins-compose.yaml --verbose config
docker compose -f jenkins-compose.yaml up -d
sleep 5
xdg-open http://localhost:8080
