#!/usr/bin/env python3
"""
Simple script to check if PostgreSQL is accessible
"""

import psycopg2
from app.config import Config

def check_postgres():
    """Check if PostgreSQL is accessible"""
    try:
        config = Config()
        print(f"Attempting to connect to: {config.DATABASE_URL}")
        
        # Parse the database URL to get connection parameters
        # Format: postgresql://user:password@host:port/database
        import re
        match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', config.DATABASE_URL)
        if not match:
            print("Invalid database URL format")
            return False
            
        user, password, host, port, database = match.groups()
        
        # Try to connect
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        print("✓ Successfully connected to PostgreSQL")
        conn.close()
        print("✓ Connection closed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to connect to PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    print("Checking PostgreSQL connectivity...")
    success = check_postgres()
    if success:
        print("\nPostgreSQL is accessible!")
    else:
        print("\nPostgreSQL is not accessible. Please check:")
        print("1. PostgreSQL service is running")
        print("2. Database 'mydb' exists")
        print("3. User 'postgres' with password 'password' has access")
        print("4. PostgreSQL is listening on port 5432")