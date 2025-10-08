#!/usr/bin/env python3
"""
Test script to verify Docker environment detection and database configuration.
This script tests that the application correctly detects its environment
and uses the appropriate database configuration.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_docker_environment_detection():
    """Test Docker environment detection logic"""
    print("Testing Docker environment detection...")
    
    # Test the is_running_in_docker function
    def is_running_in_docker():
        """Check if the application is running in a Docker container"""
        return os.path.exists('/.dockerenv') or 'HOSTNAME' in os.environ
    
    # Test environment detection
    in_docker = is_running_in_docker()
    print(f"Running in Docker: {in_docker}")
    
    # Test environment variables
    env = os.getenv('ENVIRONMENT', 'development')
    print(f"Environment: {env}")
    
    # Test database URL resolution
    database_url = os.getenv('DATABASE_URL', '')
    print(f"DATABASE_URL from environment: {database_url}")
    
    # If no DATABASE_URL is set, determine the appropriate default
    if not database_url:
        if in_docker:
            database_url = "postgresql://postgres:password@db:5432/mydb"
            print("Using Docker default PostgreSQL URL")
        else:
            if env == 'testing':
                database_url = "sqlite:///./test.db"
            elif env == 'production':
                database_url = "postgresql://user:password@localhost/prod_db"
            else:
                database_url = "sqlite:///./app/dev.db"
            print(f"Using local default URL: {database_url}")
    
    # Special handling for Docker
    if in_docker and database_url:
        original_url = database_url
        database_url = database_url.replace('127.0.0.1', 'db').replace('localhost', 'db')
        if original_url != database_url:
            print(f"Updated URL for Docker: {database_url}")
    
    print(f"Final database URL: {database_url}")
    
    # Test if we can import the actual config
    try:
        from app.config import Config
        config = Config()
        print(f"Config DATABASE_URL: {config.DATABASE_URL}")
        print("✅ Config import successful")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
    
    # Test if we can import the database module
    try:
        from app.database import engine
        print(f"Database engine URL: {engine.url}")
        print("✅ Database import successful")
    except Exception as e:
        print(f"❌ Database import failed: {e}")

if __name__ == "__main__":
    test_docker_environment_detection()