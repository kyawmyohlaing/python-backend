#!/usr/bin/env python3
"""
Test Password Verification Script
This script tests if password verification works correctly
"""

import os
import sys

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_password_verification():
    """Test password verification"""
    db = None
    try:
        # Import the database and models
        from app.database import get_db
        from app.models.user import User
        from app.security import verify_password
        
        print("Testing password verification...")
        
        # Get database session
        db = next(get_db())
        
        # Get the test user
        user = db.query(User).filter(User.username == "test").first()
        if not user:
            print("❌ Test user not found")
            return False
        
        print(f"User found: {user.username}")
        print(f"Hashed password: {user.hashed_password[:50]}...")
        
        # Test password verification
        password = "test123"
        is_valid = verify_password(password, user.hashed_password)
        
        if is_valid:
            print("✅ Password verification successful")
            return True
        else:
            print("❌ Password verification failed")
            return False
        
    except Exception as e:
        print(f"❌ Error testing password verification: {e}")
        return False
    finally:
        if db:
            try:
                db.close()
            except:
                pass

if __name__ == "__main__":
    success = test_password_verification()
    sys.exit(0 if success else 1)