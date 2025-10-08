#!/usr/bin/env python3
"""
Simple test script to verify manager login
"""

import sys
import os
import json

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@db:5432/mydb'

def test_login():
    """Test the manager login directly"""
    try:
        print("Testing manager login...")

        # Import required modules
        sys.path.append('/app')
        from app.database import engine
        from app.models.user import User
        from app.security import verify_password
        from sqlalchemy.orm import sessionmaker

        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Find the manager user
        manager_user = db.query(User).filter(User.username == 'manager').first()
        
        if not manager_user:
            print("Manager user not found!")
            return

        print(f"Found manager user: {manager_user.username}")
        print(f"Password hash: {manager_user.hashed_password}")
        
        # Test password verification
        test_password = "manager123"
        print(f"Testing password: {test_password}")
        
        try:
            is_valid = verify_password(test_password, str(manager_user.hashed_password))
            print(f"Password verification result: {is_valid}")
        except Exception as e:
            print(f"Password verification error: {str(e)}")
            import traceback
            traceback.print_exc()

        db.close()

    except Exception as e:
        print(f"Error testing login: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login()