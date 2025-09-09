# Backup Path Configuration Examples

This document provides practical examples of how to configure backup paths for different scenarios.

## 1. Using Environment Variables

### Linux/Mac:
```bash
# Set backup directory using environment variable
export BACKUP_DIR="/home/user/backups"
make backup

# Or run directly
BACKUP_DIR="/home/user/backups" ./backup_once.sh
```

### Windows (Command Prompt):
```cmd
REM Set backup directory using environment variable
set BACKUP_DIR=C:\Users\user\backups
make backup

REM Or run directly
set BACKUP_DIR=C:\Users\user\backups && backup_once.bat
```

### Windows (PowerShell):
```powershell
# Set backup directory using environment variable
$env:BACKUP_DIR="C:\Users\user\backups"
make backup

# Or run directly
$env:BACKUP_DIR="C:\Users\user\backups"; .\backup_once.bat
```

## 2. Modifying Script Directly

### Linux/Mac:
Edit `backup_once.sh`:
```bash
# Change this line in backup_once.sh
BACKUP_DIR="/path/to/your/backup/directory"  # Custom path
```

Then run:
```bash
chmod +x backup_once.sh
./backup_once.sh
```

### Windows:
Edit `backup_once.bat`:
```batch
REM Change this line in backup_once.bat
set BACKUP_DIR=C:\path\to\your\backup\directory
```

Then run:
```cmd
backup_once.bat
```

## 3. Using Absolute Paths in Commands

### Docker Volume Backup:
```bash
# Linux/Mac
docker run --rm -v postgres_data:/data -v /absolute/path/to/backups:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .

# Windows
docker run --rm -v postgres_data:/data -v C:\absolute\path\to\backups:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

### pg_dump Backup:
```bash
# Linux/Mac
docker-compose exec db pg_dump -U postgres mydb > /absolute/path/to/backups/backup_$(date +%Y%m%d_%H%M%S).sql

# Windows (PowerShell)
docker-compose exec db pg_dump -U postgres mydb > C:\absolute\path\to\backups\backup_(Get-Date -Format "yyyyMMdd_HHmmss").sql
```

## 4. Cloud Storage Integration

### AWS S3 Example:
```bash
# First create local backup
./backup_once.sh

# Then upload to S3
aws s3 cp ./backups/ s3://your-bucket/backups/ --recursive
```

### Google Cloud Storage Example:
```bash
# First create local backup
./backup_once.sh

# Then upload to GCS
gsutil cp ./backups/* gs://your-bucket/backups/
```

## 5. Network Attached Storage (NAS)

### Mount NAS and Backup:
```bash
# Linux/Mac - assuming NAS is mounted at /mnt/nas
export BACKUP_DIR="/mnt/nas/backups"
make backup

# Windows - assuming NAS is mapped to drive Z:
set BACKUP_DIR=Z:\backups
make backup
```

## 6. Backup Rotation with Custom Paths

### Enhanced backup script with rotation:
```bash
#!/bin/bash
# Custom backup script with rotation

BACKUP_DIR="/path/to/your/backups"
RETENTION_DAYS=7

# Create backup
mkdir -p "$BACKUP_DIR"
docker-compose exec db pg_dump -U postgres mydb > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"

# Remove backups older than RETENTION_DAYS
find "$BACKUP_DIR" -name "backup_*.sql" -mtime +$RETENTION_DAYS -delete
```

## 7. Multiple Environment Backups

### Development Environment:
```bash
export BACKUP_DIR="/backups/development"
make backup
```

### Production Environment:
```bash
export BACKUP_DIR="/backups/production"
make backup
```

## Best Practices for Backup Paths

1. **Use Absolute Paths**: Avoid relative paths that might change based on current directory
2. **Ensure Permissions**: Make sure the backup directory is writable by the user running the script
3. **Network Reliability**: For network paths, ensure connectivity before starting backup
4. **Disk Space Monitoring**: Check available space before creating backups
5. **Path Validation**: Validate backup paths exist before starting the backup process

## Troubleshooting Path Issues

### Common Issues and Solutions:

1. **Permission Denied**:
   ```bash
   # Fix permissions
   sudo chown $USER:$USER /path/to/backup/directory
   chmod 755 /path/to/backup/directory
   ```

2. **Path Does Not Exist**:
   ```bash
   # Create the directory
   mkdir -p /path/to/backup/directory
   ```

3. **Disk Space Full**:
   ```bash
   # Check available space
   df -h /path/to/backup/directory
   ```

4. **Network Path Issues**:
   ```bash
   # Test connectivity
   ping your-nas-or-server
   ```

These examples should help you configure backup paths according to your specific requirements and infrastructure setup.