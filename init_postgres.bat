@echo off
REM Script to initialize PostgreSQL database with tables and sample data on Windows

echo Initializing PostgreSQL database...

REM Check if we're in the right directory
if not exist app\database.py (
    echo Error: This script must be run from the python_backend_structure directory
    pause
    exit /b 1
)

REM Run the Python initialization script
python init_postgres.py

if %errorlevel% neq 0 (
    echo Error occurred during database initialization
    pause
    exit /b %errorlevel%
)

echo Database initialization completed successfully.
pause