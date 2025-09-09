#!/usr/bin/env python3
"""
Final verification script for the FastAPI backend template.
This script checks if all required components are present and correctly configured.
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

def check_required_files():
    """Check all required files"""
    print("Checking required files...")
    
    required_files = [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.override.yml",
        "requirements.txt",
        ".env.example",
        "Makefile",
        "start.sh",
        "GITHUB_README.md",
        "PROJECT_SUMMARY.md",
        "LICENSE",
        ".gitignore",
        "init_repo.sh",
        "init_repo.bat"
    ]
    
    all_passed = True
    for file in required_files:
        if not check_file_exists(file):
            all_passed = False
    
    return all_passed

def check_required_directories():
    """Check all required directories"""
    print("\nChecking required directories...")
    
    required_dirs = [
        "app",
        "app/models",
        "app/schemas",
        "app/services",
        "app/routes",
        "app/migrations",
        "app/migrations/versions",
        "tests"
    ]
    
    all_passed = True
    for dir in required_dirs:
        if not check_directory_exists(dir):
            all_passed = False
    
    return all_passed

def check_app_files():
    """Check all app files"""
    print("\nChecking app files...")
    
    app_files = [
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/security.py",
        "app/models/user.py",
        "app/schemas/user_schema.py",
        "app/services/user_service.py",
        "app/routes/user_routes.py",
        "app/migrations/alembic.ini",
        "app/migrations/env.py",
        "app/migrations/versions/0001_create_users_table.py",
        "app/migrations/versions/0002_seed_user.py"
    ]
    
    all_passed = True
    for file in app_files:
        if not check_file_exists(file):
            all_passed = False
    
    return all_passed

def check_test_files():
    """Check all test files"""
    print("\nChecking test files...")
    
    test_files = [
        "tests/__init__.py",
        "tests/test_users.py",
        "tests/test_users_postgres.py",
        "tests/conftest.py"
    ]
    
    all_passed = True
    for file in test_files:
        if not check_file_exists(file):
            all_passed = False
    
    return all_passed

def main():
    """Run all verification checks"""
    print("FastAPI Backend Template - Final Verification")
    print("=" * 50)
    
    # Run all checks
    files_ok = check_required_files()
    dirs_ok = check_required_directories()
    app_files_ok = check_app_files()
    test_files_ok = check_test_files()
    
    # Summary
    print("\n" + "=" * 50)
    print("Verification Summary:")
    print(f"Required files: {'PASS' if files_ok else 'FAIL'}")
    print(f"Required directories: {'PASS' if dirs_ok else 'FAIL'}")
    print(f"App files: {'PASS' if app_files_ok else 'FAIL'}")
    print(f"Test files: {'PASS' if test_files_ok else 'FAIL'}")
    
    if files_ok and dirs_ok and app_files_ok and test_files_ok:
        print("\n✓ All checks passed! Your FastAPI backend template is ready.")
        print("\nNext steps:")
        print("1. Initialize git repository: ./init_repo.sh (or init_repo.bat on Windows)")
        print("2. Copy .env.example to .env and update values if needed")
        print("3. Start development: make dev")
        print("4. Test the API with the seeded example user:")
        print("   - Email: user@example.com")
        print("   - Password: password123")
        return 0
    else:
        print("\n✗ Some checks failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())