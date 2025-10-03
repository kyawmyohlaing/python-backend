#!/usr/bin/env python3
"""
Script to check existing users in the database using local configuration
"""

import sys
import os

# Load local environment variables
from dotenv import load_dotenv
load_dotenv('.env.local')

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def check_users():
    """Check existing users in the database"""
    try:
        # Import database components
        from app.database import engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        
        print(f"Connecting to database: {engine.url}")
        
        # Create a database session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Query all users
        users = db.query(User).all()
        
        print("Existing Users in Database:")
        print("=" * 40)
        
        if not users:
            print("No users found in the database")
            db.close()
            return
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Created At: {user.created_at}")
            print("-" * 30)
            
        db.close()
            
    except Exception as e:
        print(f"Error checking users: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_users()