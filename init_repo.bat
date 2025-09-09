@echo off
REM Script to initialize the git repository

echo Initializing git repository...

REM Initialize git repository
git init

REM Add all files
git add .

REM Make the first commit
git commit -m "Initial commit: FastAPI backend template with PostgreSQL, Alembic, JWT auth, and Docker"

REM Create main branch
git branch -M main

echo Git repository initialized successfully!
echo.
echo To push to GitHub:
echo 1. Create a new repository on GitHub
echo 2. Run: git remote add origin ^<your-github-repo-url^>
echo 3. Run: git push -u origin main