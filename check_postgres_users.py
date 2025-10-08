#!/usr/bin/env python3
"""
Script to check users in the PostgreSQL database
"""

import sys
import os

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@localhost:5432/mydb'

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def check_users():
    """Check users in the PostgreSQL database"""
    try:
        # Import required modules
        from app.database import engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        
        print(f"Connecting to database: {engine.url}")
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get all users
        users = db.query(User).all()
        
        print("Users in PostgreSQL database:")
        print("=============================")
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Password hash: {user.hashed_password}")
            print(f"Password hash length: {len(str(user.hashed_password)) if user.hashed_password else 0}")
            print("---")
        
        db.close()
        
    except Exception as e:
        print(f"Error checking users: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_users()