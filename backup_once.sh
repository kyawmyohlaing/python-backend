#!/bin/bash

# Simple one-time backup script
# Run this script to create an immediate backup of your PostgreSQL database

# Configuration - Modify these variables to set your custom paths
CONTAINER_NAME=$(docker-compose ps -q db)
BACKUP_DIR="${BACKUP_DIR:-./backups}"  # Default to ./backups, but can be overridden by environment variable
DB_USER="postgres"
DB_NAME="mydb"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="backup_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if container is running
if [ -z "$CONTAINER_NAME" ]; then
    echo "Error: Database container not found. Make sure your services are running."
    echo "Start services with: docker-compose up -d"
    exit 1
fi

echo "Creating backup of PostgreSQL database..."
echo "Backup will be saved to: $BACKUP_DIR/$BACKUP_FILE"

# Perform backup
docker exec -t "$CONTAINER_NAME" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup successful!"
    echo "Backup saved as: $BACKUP_DIR/$BACKUP_FILE"
    echo "Backup size: $(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)"
else
    echo "Backup failed!"
    exit 1
fi

echo "Backup process completed."