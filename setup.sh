#!/bin/bash

# Setup script for the FastAPI backend with Docker

echo "Setting up the FastAPI backend environment..."

# Check if .env file exists, if not create it from .env.example
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ".env file created. Please review and update the values if needed."
else
    echo ".env file already exists. Skipping creation."
fi

echo "Setup complete!"
echo ""
echo "To start the services, run:"
echo "  docker-compose up --build"
echo ""
echo "The application will be available at http://localhost:8088"