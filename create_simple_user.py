#!/usr/bin/env python3
"""
Create Simple Test User Script
This script creates a test user with proper password hashing
"""

import os
import sys
from datetime import datetime

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def create_simple_user():
    """Create a test user with proper password hashing"""
    db = None
    try:
        # Import the database and models
        from app.database import get_db
        from app.models.user import User, UserRole
        from app.security import hash_password
        
        print("Creating simple test user with proper hashing...")
        
        # Get database session
        db = next(get_db())
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "test").first()
        if existing_user:
            print("User 'test' already exists, deleting...")
            db.delete(existing_user)
            db.commit()
        
        # Hash the password properly
        hashed_password = hash_password("test123")
        
        # Create new user
        test_user = User(
            username="test",
            email="test@example.com",
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            full_name="Test User",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add to database
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ Test user created successfully")
        print(f"  - ID: {test_user.id}")
        print(f"  - Username: {test_user.username}")
        print(f"  - Role: {test_user.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        if db:
            db.rollback()
        return False
    finally:
        if db:
            try:
                db.close()
            except:
                pass

if __name__ == "__main__":
    success = create_simple_user()
    sys.exit(0 if success else 1)