#!/usr/bin/env python3
"""
Test script to check Docker PostgreSQL database connection
"""

import psycopg2
import os
from dotenv import load_dotenv

def test_docker_db_connection():
    """Test Docker database connection"""
    try:
        print("Attempting to connect to Docker PostgreSQL database...")
        print("Using connection string: postgresql://postgres:password@localhost:5432/mydb")
        
        # Attempt connection directly to localhost (when Docker maps port 5432)
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mydb",
            user="postgres",
            password="password"
        )
        
        print("✅ Successfully connected to Docker PostgreSQL database!")
        
        # Test with a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        # Check if database is initialized
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = cursor.fetchall()
        print(f"Existing tables: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Docker is installed and running")
        print("2. Ensure the PostgreSQL container is running: docker-compose up -d db")
        print("3. Check if port 5432 is available and not blocked by a firewall")
        print("4. Verify database credentials match docker-compose.yml")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_docker_db_connection()