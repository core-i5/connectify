#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt-get update -y

# Install prerequisites
echo "Installing prerequisites..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Install Docker
echo "Installing Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce

# Add current user to the Docker group
echo "Adding current user to the Docker group..."
sudo usermod -aG docker ${USER}

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version
docker-compose --version

# Install Nginx
echo "Installing Nginx..."
sudo apt-get install -y nginx

# Start and enable Nginx
echo "Starting and enabling Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

# Print installation completion message
echo "System-level dependencies installed successfully!"
echo "Please log out and log back in to apply Docker group changes."

# Optionally, reboot the system
echo "Rebooting the system to apply changes..."
sudo reboot
