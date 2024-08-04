#!/bin/bash

# Define and export environment variables
export POSTGRES_DB="connectify"
export POSTGRES_USER="connectify"
export POSTGRES_PASSWORD="connectify"

# Clone the repository
echo "Cloning the repository..."
# Replace <your-repo-url> with the actual URL
git clone https://github.com/core-i5/connectify.git
cd connectify || exit

# Build Docker images
echo "Building Docker images..."
docker-compose build --no-cache

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

# Install Python dependencies for user_service
echo "Installing dependencies for user_service..."
docker-compose exec user_service pip install -r requirements.txt

# Install Python dependencies for post_service
echo "Installing dependencies for post_service..."
docker-compose exec post_service pip install -r requirements.txt

# Apply migrations for user_service
echo "Create and applying migrations for user_service..."
docker-compose exec user_service python3 manage.py makemigrations
docker-compose exec user_service python3 manage.py migrate

# Apply migrations for post_service
echo "Create and applying migrations for post_service..."
docker-compose exec post_service python3 manage.py makemigrations
docker-compose exec post_service python3 manage.py migrate

# # Create a superuser for user_service
# echo "Creating a superuser for user_service..."
# docker-compose exec user_service python3 manage.py createsuperuser

# # Create a superuser for post_service
# echo "Creating a superuser for post_service..."
# docker-compose exec post_service python3 manage.py createsuperuser

# Elasticsearch health check (optional)
echo "Checking Elasticsearch health status..."
curl -X GET "localhost:9200/_cluster/health?pretty"

echo "Setup completed successfully!"
