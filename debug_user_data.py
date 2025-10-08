#!/usr/bin/env python3
"""
Script to debug user data in detail
"""

import sys
import os

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import engine
    from app.models.user import User
except ImportError:
    # Try importing directly (Docker container)
    from database import engine
    from models import User

from sqlalchemy.orm import sessionmaker

def debug_user_data():
    try:
        print("Debugging user data...")
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get the manager user
        manager_user = db.query(User).filter(User.username == 'manager').first()
        
        if not manager_user:
            print("Manager user not found!")
            return
            
        print(f"User ID: {manager_user.id}")
        print(f"Username: {manager_user.username}")
        print(f"Email: {manager_user.email}")
        print(f"Role: {manager_user.role}")
        print(f"Hashed password type: {type(manager_user.hashed_password)}")
        print(f"Hashed password length: {len(str(manager_user.hashed_password))}")
        print(f"Hashed password: {manager_user.hashed_password}")
        print(f"Full name: {manager_user.full_name}")
        print(f"Created at: {manager_user.created_at}")
        print(f"Updated at: {manager_user.updated_at}")
        
        # Check if the user can also be found by email
        email_user = db.query(User).filter(User.email == 'manager@example.com').first()
        if email_user:
            print(f"User found by email - ID: {email_user.id}, Username: {email_user.username}")
            print(f"Email user hashed password: {email_user.hashed_password}")
            print(f"Same user object: {manager_user.id == email_user.id}")
        else:
            print("User not found by email")
        
        db.close()
        
    except Exception as e:
        print(f"Error debugging user data: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_user_data()