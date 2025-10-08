#!/usr/bin/env python3
"""
Script to test the manager user's password
"""

import sys
import os

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import engine
    from app.models.user import User
    from app.security import verify_password
except ImportError:
    # Try importing directly (Docker container)
    from database import engine
    from models import User
    from security import verify_password

from sqlalchemy.orm import sessionmaker

def test_manager_password():
    try:
        print("Testing manager user password...")
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get the manager user
        manager_user = db.query(User).filter(User.username == 'manager').first()
        
        if not manager_user:
            print("Manager user not found!")
            return
            
        print(f"User: {manager_user.username}")
        print(f"Email: {manager_user.email}")
        print(f"Hashed password: {manager_user.hashed_password}")
        
        # Test password verification
        test_password = "manager123"
        print(f"Testing password: {test_password}")
        
        is_valid = verify_password(test_password, manager_user.hashed_password)
        print(f"Password verification result: {is_valid}")
        
        # Also test with email as identifier
        test_email = "manager@example.com"
        print(f"Testing with email as identifier: {test_email}")
        email_user = db.query(User).filter(User.email == test_email).first()
        if email_user:
            print(f"User found by email: {email_user.username}")
            email_valid = verify_password(test_password, email_user.hashed_password)
            print(f"Password verification with email: {email_valid}")
        else:
            print("User not found by email")
        
        db.close()
        
    except Exception as e:
        print(f"Error testing manager password: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_manager_password()