@echo off
REM Simple one-time backup script for Windows
REM Run this script to create an immediate backup of your PostgreSQL database

REM Configuration - Modify these variables to set your custom paths
for /f "delims=" %%i in ('docker-compose ps -q db') do set CONTAINER_ID=%%i
set BACKUP_DIR=%BACKUP_DIR%
if "%BACKUP_DIR%"=="" set BACKUP_DIR=backups
set DB_USER=postgres
set DB_NAME=mydb

REM Generate timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set TIMESTAMP=%dt:~0,4%%dt:~4,2%%dt:~6,2%_%dt:~8,2%%dt:~10,2%%dt:~12,2%

REM Replace spaces and colons in filename (Windows compatibility)
set TIMESTAMP=%TIMESTAMP: =0%
set TIMESTAMP=%TIMESTAMP::=%

set BACKUP_FILE=backup_%TIMESTAMP%.sql

REM Create backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Check if container is running
if "%CONTAINER_ID%"=="" (
    echo Error: Database container not found. Make sure your services are running.
    echo Start services with: docker-compose up -d
    exit /b 1
)

echo Creating backup of PostgreSQL database...
echo Backup will be saved to: %BACKUP_DIR%\%BACKUP_FILE%

REM Perform backup
docker exec -t %CONTAINER_ID% pg_dump -U %DB_USER% %DB_NAME% > "%BACKUP_DIR%\%BACKUP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo Backup successful!
    echo Backup saved as: %BACKUP_DIR%\%BACKUP_FILE%
    for %%A in ("%BACKUP_DIR%\%BACKUP_FILE%") do echo Backup size: %%~zA bytes
) else (
    echo Backup failed!
    exit /b 1
)

echo Backup process completed.