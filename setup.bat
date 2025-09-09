@echo off
REM Setup script for the FastAPI backend with Docker on Windows

echo Setting up the FastAPI backend environment...

REM Check if .env file exists, if not create it from .env.example
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created. Please review and update the values if needed.
) else (
    echo .env file already exists. Skipping creation.
)

echo Setup complete!
echo.
echo To start the services, run:
echo   docker-compose up --build
echo.
echo The application will be available at http://localhost:8088