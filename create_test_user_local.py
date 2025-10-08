#!/usr/bin/env python3
"""
Create Test User Script
This script creates a test user in the local database
"""

import os
import sys
from datetime import datetime

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def truncate_password_for_bcrypt(password: str) -> str:
    """
    Truncate password to 72 bytes for bcrypt compatibility.
    Bcrypt has a limitation where only the first 72 bytes are used.
    """
    MAX_PASSWORD_LENGTH = 72
    if isinstance(password, str):
        # Encode to bytes to check actual byte length
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > MAX_PASSWORD_LENGTH:
            # Truncate to 72 bytes and decode back to string
            truncated_bytes = password_bytes[:MAX_PASSWORD_LENGTH]
            return truncated_bytes.decode('utf-8', errors='ignore')
    return password

def create_test_user():
    """Create a test user"""
    db = None
    try:
        # Import the database and models
        from app.database import get_db
        from app.models.user import User, UserRole
        from passlib.context import CryptContext
        
        print("Creating test user...")
        
        # Create password context
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Get database session
        db = next(get_db())
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("User 'admin' already exists")
            return True
        
        # Create new user with truncated password
        truncated_password = truncate_password_for_bcrypt("admin")
        hashed_password = pwd_context.hash(truncated_password)
        test_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            full_name="Administrator",
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
    success = create_test_user()
    sys.exit(0 if success else 1)