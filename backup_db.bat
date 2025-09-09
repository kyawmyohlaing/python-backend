@echo off
REM PostgreSQL Docker Backup Script for Windows
REM This script creates a backup of the PostgreSQL database running in Docker

REM Configuration
set CONTAINER_NAME=python_backend_structure_db_1
set DB_USER=postgres
set DB_NAME=mydb
set BACKUP_DIR=backups
set DATE=%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_FILE=postgres_backup_%DATE%.sql

REM Replace spaces and colons in filename (Windows compatibility)
set BACKUP_FILE=%BACKUP_FILE: =0%
set BACKUP_FILE=%BACKUP_FILE::=%

REM Create backup directory if it doesn't exist
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

echo Starting PostgreSQL backup...

REM Create backup using pg_dump
docker exec -t %CONTAINER_NAME% pg_dump -U %DB_USER% %DB_NAME% > %BACKUP_DIR%\%BACKUP_FILE%

if %ERRORLEVEL% EQU 0 (
    echo Backup successful: %BACKUP_DIR%\%BACKUP_FILE%
    for %%A in (%BACKUP_DIR%\%BACKUP_FILE%) do echo Backup size: %%~zA bytes
) else (
    echo Backup failed!
    exit /b 1
)

echo Backup process completed.