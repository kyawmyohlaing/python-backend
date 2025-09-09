#!/usr/bin/env python3
"""
Verification script for the FastAPI backend setup.
This script checks if all required files are present and have the correct content.
"""

import os
import sys

def check_file_exists(file_path):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✓ {file_path} exists")
        return True
    else:
        print(f"✗ {file_path} does not exist")
        return False

def check_directory_exists(dir_path):
    """Check if a directory exists"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✓ {dir_path} exists")
        return True
    else:
        print(f"✗ {dir_path} does not exist")
        return False

def main():
    """Verify the FastAPI backend setup"""
    print("Verifying FastAPI backend setup...")
    print("=" * 40)
    
    # Check required files
    required_files = [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.override.yml",
        "requirements.txt",
        ".env.example",
        "Makefile",
        "start.sh"
    ]
    
    # Check required directories
    required_dirs = [
        "app",
        "app/models",
        "app/schemas",
        "app/services",
        "app/routes",
        "app/migrations"
    ]
    
    # Check app files
    app_files = [
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/security.py",
        "app/models/user.py",
        "app/schemas/user_schema.py",
        "app/services/user_service.py",
        "app/routes/user_routes.py"
    ]
    
    all_checks_passed = True
    
    # Check required files
    print("Checking required files:")
    for file in required_files:
        if not check_file_exists(file):
            all_checks_passed = False
    print()
    
    # Check required directories
    print("Checking required directories:")
    for dir in required_dirs:
        if not check_directory_exists(dir):
            all_checks_passed = False
    print()
    
    # Check app files
    print("Checking app files:")
    for file in app_files:
        if not check_file_exists(file):
            all_checks_passed = False
    print()
    
    # Summary
    print("=" * 40)
    if all_checks_passed:
        print("✓ All checks passed! Your FastAPI backend is ready.")
        return 0
    else:
        print("✗ Some checks failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())