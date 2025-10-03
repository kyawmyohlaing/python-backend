#!/usr/bin/env python3
"""
Test Authentication Service Script
This script tests the authentication service directly
"""

import os
import sys

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_auth_service():
    """Test the authentication service directly"""
    db = None
    try:
        # Import the database and models
        from app.database import get_db
        from app.services.user_service import UserService
        
        print("Testing authentication service directly...")
        
        # Get database session
        db = next(get_db())
        
        # Test authentication with test user
        username = "test"
        password = "test123"
        
        print(f"Attempting to authenticate user: {username}")
        
        user = UserService.authenticate_user(db, username, password)
        
        if user:
            print(f"✅ Authentication successful!")
            print(f"  User ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Role: {user.role}")
            return True
        else:
            print("❌ Authentication failed")
            return False
        
    except Exception as e:
        print(f"❌ Error testing authentication service: {e}")
        return False
    finally:
        if db:
            try:
                db.close()
            except:
                pass

if __name__ == "__main__":
    success = test_auth_service()
    sys.exit(0 if success else 1)