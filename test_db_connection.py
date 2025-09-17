#!/usr/bin/env python3
"""
Database Connection Test Script

This script helps verify that the PostgreSQL database connection is properly configured.
It tests the connection using the credentials from the .env file.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connectivity with detailed diagnostics"""
    print("🔍 Testing Database Connection...")
    print("=" * 50)
    
    # Check if required environment variables are set
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("💡 Please ensure you have a .env file with DATABASE_URL configured")
        return False
    
    print(f"📄 DATABASE_URL: {database_url}")
    
    # Parse database URL for better diagnostics
    try:
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        print(f"👤 Username: {parsed.username}")
        print(f"🌐 Host: {parsed.hostname}")
        print(f"📍 Port: {parsed.port}")
        print(f"🗄️  Database: {parsed.path[1:] if parsed.path.startswith('/') else parsed.path}")
    except Exception as e:
        print(f"⚠️  Could not parse DATABASE_URL: {e}")
    
    # Test database connection
    try:
        print("\n🔄 Attempting to connect to database...")
        import psycopg2
        
        # Extract connection parameters
        from sqlalchemy import create_engine, text
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version(), current_database(), current_user;"))
            row = result.fetchone()
            if row:
                version, database, user = row
            else:
                print("❌ No data returned from database query")
                return False
        
        print(f"✅ Connection successful!")
        print(f"🐘 PostgreSQL Version: {version}")
        print(f"🗄️  Connected Database: {database}")
        print(f"👤 Connected User: {user}")
        
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed")
        print("💡 Install it with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        
        # Provide specific troubleshooting advice
        if "password authentication failed" in str(e):
            print("\n🔧 Troubleshooting Tips:")
            print("1. Check if your PostgreSQL credentials are correct in .env")
            print("2. If you changed credentials, reset the database volume:")
            print("   docker-compose down -v")
            print("   make dev")
            print("3. Manually set the PostgreSQL password:")
            print("   docker-compose exec db psql -U postgres")
            print("   \\password postgres")
            print("   (Enter 'password' when prompted)")
        elif "Connection refused" in str(e):
            print("\n🔧 Troubleshooting Tips:")
            print("1. Ensure PostgreSQL is running")
            print("2. Check if you're using the correct host (localhost vs db)")
            print("3. Verify the PostgreSQL port is accessible")
        else:
            print("\n🔧 General Troubleshooting:")
            print("1. Check your .env file configuration")
            print("2. Ensure Docker is running (if using Docker)")
            print("3. Verify PostgreSQL service is accessible")
        
        return False

def check_env_file():
    """Check if .env file exists and has basic configuration"""
    print("\n📂 Checking .env file...")
    print("-" * 30)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("💡 Copy .env.example to .env and configure it:")
        print("   cp .env.example .env")
        return False
    
    print("✅ .env file found")
    
    # Check for required variables
    required_vars = ['DATABASE_URL']
    missing_vars = []
    
    with open('.env', 'r') as f:
        content = f.read()
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing variables in .env: {', '.join(missing_vars)}")
        return False
    
    print("✅ Required variables found in .env")
    return True

def main():
    """Main function"""
    print("🚀 FastAPI Backend Database Connection Test")
    print("=" * 60)
    
    # Check .env file
    if not check_env_file():
        sys.exit(1)
    
    print()
    
    # Test database connection
    success = test_database_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Database connection is working correctly.")
        print("💡 You can now start the application with: make dev")
    else:
        print("💥 Database connection test failed.")
        print("💡 Please check the troubleshooting guide: TROUBLESHOOTING.md")
        sys.exit(1)

if __name__ == "__main__":
    main()