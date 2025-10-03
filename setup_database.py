#!/usr/bin/env python3
"""
Script to set up the PostgreSQL database for the application
"""

import psycopg2
import sys
import os

def setup_database():
    """Set up the PostgreSQL database"""
    try:
        # First, connect to the default PostgreSQL database to create our database
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",  # Default database
            user="postgres",
            password="postgres"  # Default password, might need to be changed
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if our database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'mydb'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating database 'mydb'...")
            cursor.execute("CREATE DATABASE mydb")
            print("✅ Database 'mydb' created successfully")
        else:
            print("Database 'mydb' already exists")
        
        cursor.close()
        conn.close()
        
        # Now connect to our database and create a user
        print("Connecting to 'mydb' database...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mydb",
            user="postgres",
            password="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create user if not exists
        try:
            cursor.execute("CREATE USER postgres WITH PASSWORD 'password'")
            print("✅ User 'postgres' created successfully")
        except psycopg2.Error as e:
            if "already exists" in str(e):
                print("User 'postgres' already exists")
                # Update password
                cursor.execute("ALTER USER postgres WITH PASSWORD 'password'")
                print("✅ User 'postgres' password updated")
            else:
                print(f"Note: {e}")
        
        # Grant privileges
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE mydb TO postgres")
        print("✅ Privileges granted to user 'postgres'")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database setup completed successfully!")
        print("\nDatabase details:")
        print("  Host: localhost")
        print("  Port: 5432")
        print("  Database: mydb")
        print("  User: postgres")
        print("  Password: password")
        
    except psycopg2.OperationalError as e:
        if "authentication failed" in str(e).lower():
            print("❌ Authentication failed. Common solutions:")
            print("1. Check if PostgreSQL is running")
            print("2. Try finding your PostgreSQL password:")
            print("   - On Windows: Check PostgreSQL installation or reset password")
            print("   - On macOS: Try 'postgres' as password or check Postgres.app")
            print("   - On Linux: Try your system password or 'postgres'")
            print("\nYou can also try connecting with a PostgreSQL management tool")
            print("like pgAdmin to verify your credentials.")
        else:
            print(f"❌ Database connection failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_database()#!/usr/bin/env python3
"""
Script to set up the PostgreSQL database for the application
"""

import psycopg2
import sys
import os

def setup_database():
    """Set up the PostgreSQL database"""
    try:
        # First, connect to the default PostgreSQL database to create our database
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",  # Default database
            user="postgres",
            password="postgres"  # Default password, might need to be changed
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if our database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'mydb'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating database 'mydb'...")
            cursor.execute("CREATE DATABASE mydb")
            print("✅ Database 'mydb' created successfully")
        else:
            print("Database 'mydb' already exists")
        
        cursor.close()
        conn.close()
        
        # Now connect to our database and create a user
        print("Connecting to 'mydb' database...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mydb",
            user="postgres",
            password="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create user if not exists
        try:
            cursor.execute("CREATE USER postgres WITH PASSWORD 'password'")
            print("✅ User 'postgres' created successfully")
        except psycopg2.Error as e:
            if "already exists" in str(e):
                print("User 'postgres' already exists")
                # Update password
                cursor.execute("ALTER USER postgres WITH PASSWORD 'password'")
                print("✅ User 'postgres' password updated")
            else:
                print(f"Note: {e}")
        
        # Grant privileges
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE mydb TO postgres")
        print("✅ Privileges granted to user 'postgres'")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database setup completed successfully!")
        print("\nDatabase details:")
        print("  Host: localhost")
        print("  Port: 5432")
        print("  Database: mydb")
        print("  User: postgres")
        print("  Password: password")
        
    except psycopg2.OperationalError as e:
        if "authentication failed" in str(e).lower():
            print("❌ Authentication failed. Common solutions:")
            print("1. Check if PostgreSQL is running")
            print("2. Try finding your PostgreSQL password:")
            print("   - On Windows: Check PostgreSQL installation or reset password")
            print("   - On macOS: Try 'postgres' as password or check Postgres.app")
            print("   - On Linux: Try your system password or 'postgres'")
            print("\nYou can also try connecting with a PostgreSQL management tool")
            print("like pgAdmin to verify your credentials.")
        else:
            print(f"❌ Database connection failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_database()