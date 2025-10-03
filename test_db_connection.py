#!/usr/bin/env python3
"""
Test script to check PostgreSQL database connection
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv('.env.local')

def test_db_connection():
    """Test database connection"""
    try:
        # Get database URL from environment
        database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/mydb')
        print(f"Attempting to connect to: {database_url}")
        
        # Parse the database URL
        # Format: postgresql://user:password@host:port/database
        import re
        match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', database_url)
        if not match:
            print("Invalid database URL format")
            return
            
        user, password, host, port, database = match.groups()
        
        print(f"Connecting to PostgreSQL database:")
        print(f"  Host: {host}")
        print(f"  Port: {port}")
        print(f"  Database: {database}")
        print(f"  User: {user}")
        
        # Attempt connection
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        print("✅ Successfully connected to PostgreSQL database!")
        
        # Test with a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is installed and running")
        print("2. Check if PostgreSQL is listening on port 5432")
        print("3. Verify database credentials in .env.local")
        print("4. Ensure the 'mydb' database exists")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_db_connection()
