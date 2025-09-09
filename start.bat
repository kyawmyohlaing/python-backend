@echo off
REM Script to start the FastAPI backend services

REM Check if .env file exists, if not create it from .env.example
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created. Please review and update the values if needed.
) else (
    echo .env file already exists. Skipping creation.
)

REM Check if running in development or production mode
if "%1"=="prod" (
    echo Starting services in production mode...
    docker-compose -f docker-compose.yml up --build -d
) else (
    echo Starting services in development mode...
    docker-compose up --build
)

echo.
echo The application will be available at http://localhost:8088
echo The database will be available at localhost:5432