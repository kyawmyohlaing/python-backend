#!/usr/bin/env python3
"""
Simple User Check Script
This script checks if we can connect to the database and find users
"""

import os
import sys

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def check_users():
    """Check if we can connect to the database and find users"""
    db = None
    try:
        # Import the database and models
        from app.database import get_db
        from app.models.user import User

        print("Connecting to database...")
        
        # Get database session
        db = next(get_db())
        
        # Try to query users
        users = db.query(User).all()
        
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  - ID: {user.id}, Username: {user.username}, Role: {user.role}")
            
        return True
        
    except Exception as e:
        print(f"Error checking users: {e}")
        return False
    finally:
        if db:
            try:
                db.close()
            except:
                pass

if __name__ == "__main__":
    success = check_users()
    sys.exit(0 if success else 1)