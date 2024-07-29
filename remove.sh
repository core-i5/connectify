#!/bin/bash

# Warning Message
echo "WARNING: This script will stop and remove all Docker containers, images, networks, and volumes not currently in use by a container."
echo "If this is not intended, please close this script immediately. Waiting for 10 seconds..."
sleep 10

# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Run Docker system prune
docker system prune -a --volumes -f

# Rebuild and bring up Docker Compose services without using cache
# docker-compose up --build --no-cache -d