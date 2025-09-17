@echo off
REM Kitchen Orders Migration Script for Windows/Docker

echo === Kitchen Orders Migration for Windows/Docker ===

REM Test database connection
echo Testing database connection...
python test_db_connection.py

if %errorlevel% neq 0 (
    echo Database connection test failed. Please check your database configuration.
    exit /b 1
)

REM Run migration
echo Running kitchen orders table migration...
python migrations/create_kitchen_orders_table.py

if %errorlevel% equ 0 (
    echo ✅ Migration completed successfully!
    echo You can now restart your application to use the database-backed kitchen orders system.
) else (
    echo ❌ Migration failed!
    exit /b 1
)