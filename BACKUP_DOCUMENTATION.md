# PostgreSQL Database Backup Documentation

This document provides comprehensive instructions for backing up and restoring the PostgreSQL database used in the FastAPI backend template. The backup strategies ensure data persistence and disaster recovery for your application.

## Table of Contents

1. [Overview](#overview)
2. [Backup Methods](#backup-methods)
   - [Docker Volume Backup](#docker-volume-backup)
   - [pg_dump Database Backup](#pg_dump-database-backup)
   - [Automated Backup Scripts](#automated-backup-scripts)
3. [Using Backup Scripts](#using-backup-scripts)
   - [One-time Backup](#one-time-backup)
   - [Scheduled Backups](#scheduled-backups)
4. [Makefile Integration](#makefile-integration)
5. [Restoring from Backup](#restoring-from-backup)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Overview

The FastAPI backend template uses PostgreSQL as its primary database, running in a Docker container. The database data is persisted using Docker volumes, ensuring data survives container restarts. However, additional backup strategies are necessary for disaster recovery and data migration purposes.

## Backup Methods

### Docker Volume Backup

This method creates a backup of the entire Docker volume containing the PostgreSQL data files.

**Backup Command (with custom path):**
```bash
# For Linux/Mac - backup to a specific directory
docker run --rm -v postgres_data:/data -v /path/to/your/backup/directory:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .

# For Windows - backup to a specific directory
docker run --rm -v postgres_data:/data -v C:\path\to\your\backup\directory:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

**Restore Command (with custom path):**
```bash
# For Linux/Mac - restore from a specific directory
docker run --rm -v postgres_data_new:/data -v /path/to/your/backup/directory:/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data

# For Windows - restore from a specific directory
docker run --rm -v postgres_data_new:/data -v C:\path\to\your\backup\directory:/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```

### pg_dump Database Backup

This is the recommended approach for PostgreSQL backups as it creates logical backups that are portable across different PostgreSQL versions.

**Backup Command (with custom path):**
```bash
# Backup to a specific directory with custom filename
docker-compose exec db pg_dump -U postgres mydb > /path/to/your/backup/directory/backup_$(date +%Y%m%d_%H%M%S).sql

# For Windows (PowerShell)
docker-compose exec db pg_dump -U postgres mydb > C:\path\to\your\backup\directory\backup_(Get-Date -Format "yyyyMMdd_HHmmss").sql
```

**Restore Command (with custom path):**
```bash
# Restore from a specific backup file
docker-compose exec -T db psql -U postgres mydb < /path/to/your/backup/directory/backup_filename.sql

# For Windows
docker-compose exec -T db psql -U postgres mydb < C:\path\to\your\backup\directory\backup_filename.sql
```

### Automated Backup Scripts

The template includes several scripts to automate the backup process:
- `backup_once.sh` / `backup_once.bat` - One-time backup script
- `backup_db.sh` / `backup_db.bat` - Configurable backup script with retention policy

## Using Backup Scripts

### One-time Backup

#### Linux/Mac:
1. Ensure your services are running:
   ```bash
   docker-compose up -d
   ```
2. Make the script executable:
   ```bash
   chmod +x backup_once.sh
   ```
3. Edit the script to set your custom backup path:
   ```bash
   # In backup_once.sh, modify the BACKUP_DIR variable
   BACKUP_DIR="/path/to/your/backup/directory"
   ```
4. Run the backup:
   ```bash
   ./backup_once.sh
   ```

#### Windows:
1. Ensure your services are running:
   ```cmd
   docker-compose up -d
   ```
2. Edit the batch script to set your custom backup path:
   ```cmd
   REM In backup_once.bat, modify the BACKUP_DIR variable
   set BACKUP_DIR=C:\path\to\your\backup\directory
   ```
3. Run the backup script:
   ```cmd
   backup_once.bat
   ```

The backup will be saved in your specified directory with a timestamp in the filename.

### Scheduled Backups

#### Linux/Mac (using cron):
1. Edit your crontab:
   ```bash
   crontab -e
   ```
2. Add a line to run the backup daily at 2 AM:
   ```bash
   0 2 * * * /path/to/your/project/backup_once.sh
   ```

#### Windows (using Task Scheduler):
1. Open Task Scheduler
2. Create a new task
3. Set the trigger to your desired schedule
4. Set the action to run `backup_once.bat`

## Makefile Integration

The template includes a convenient Makefile command for creating backups:

```bash
make backup
```

To customize the backup path when using the Makefile:

1. Edit the backup_once.sh or backup_once.bat script to set your desired backup directory
2. Run the backup command:
   ```bash
   make backup
   ```

For more detailed examples of configuring backup paths, see [BACKUP_PATH_EXAMPLES.md](BACKUP_PATH_EXAMPLES.md).

## Restoring from Backup

To restore your database from a backup:

1. Ensure your database container is running:
   ```bash
   docker-compose up -d
   ```

2. Restore from a specific backup file:
   ```bash
   docker-compose exec -T db psql -U postgres mydb < backups/backup_20230101_120000.sql
   ```

**Important Notes:**
- Restoring will overwrite existing data
- Ensure the database schema is compatible with your application version
- Consider making a backup before restoring as a precaution

## Best Practices

1. **Regular Backups**: Schedule automated backups based on your data change frequency
2. **Multiple Backup Locations**: Store backups in multiple locations (local, cloud storage)
3. **Test Restores**: Periodically test restoring from backups to ensure they work correctly
4. **Backup Encryption**: For sensitive data, consider encrypting backup files
5. **Retention Policy**: Implement a retention policy to manage disk space (current scripts keep last 7 backups)
6. **Monitor Backup Success**: Set up notifications to alert you of backup failures
7. **Version Control**: Keep backup scripts in version control but exclude actual backup files

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**:
   - Ensure the backup directory has proper write permissions
   - On Linux/Mac, use `chmod` to set appropriate permissions

2. **Container Not Found**:
   - Verify services are running with `docker-compose ps`
   - Check the container name matches the one in the script

3. **Connection Refused**:
   - Ensure PostgreSQL is accepting connections
   - Check database credentials in the scripts

4. **Large Database Backups**:
   - For very large databases, consider using compression
   - Monitor available disk space during backup

### Useful Commands

Check running containers:
```bash
docker-compose ps
```

View container logs:
```bash
docker-compose logs db
```

Access database container shell:
```bash
docker-compose exec db bash
```

Check backup file size:
```bash
ls -lh backups/
```

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

For issues not covered in this documentation, please refer to the official documentation of the respective tools or open an issue in the repository.