#!/bin/bash

# PostgreSQL Docker Backup Script
# This script creates a backup of the PostgreSQL database running in Docker

# Configuration
CONTAINER_NAME="python_backend_structure_db_1"  # Update this to match your container name
DB_USER="postgres"
DB_NAME="mydb"
BACKUP_DIR="./backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="postgres_backup_${DATE}.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Starting PostgreSQL backup..."

# Create backup using pg_dump
docker exec -t $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/$BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_DIR/$BACKUP_FILE"
    echo "Backup size: $(du -h $BACKUP_DIR/$BACKUP_FILE | cut -f1)"
else
    echo "Backup failed!"
    exit 1
fi

# Keep only last 7 backups
echo "Cleaning up old backups (keeping last 7)..."
cd $BACKUP_DIR
ls -t postgres_backup_*.sql | tail -n +8 | xargs rm -f

echo "Backup process completed."