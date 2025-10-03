#!/usr/bin/env python3
"""
Create Database Tables Script
This script creates the necessary database tables
"""

import os
import sys

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def create_tables():
    """Create database tables"""
    try:
        print("Creating database tables...")
        
        # Import the database and models
        from app.database import Base, engine
        from app.models.user import User
        from app.models.menu import MenuItem
        from app.models.table import Table
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)