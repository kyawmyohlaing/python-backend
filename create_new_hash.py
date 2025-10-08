#!/usr/bin/env python3
"""
Script to create a new hash and update the manager user
"""

import sys
import os

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@db:5432/mydb'

def create_new_hash():
    """Create a new hash and update the manager user"""
    try:
        print("Creating new hash for manager user...")
        
        # Import required modules
        sys.path.append('/app')
        from app.database import engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        from passlib.context import CryptContext
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get the manager user
        manager_user = db.query(User).filter(User.username == 'manager').first()
        
        if not manager_user:
            print("Manager user not found!")
            return
            
        print(f"User: {manager_user.username}")
        print(f"Current hashed password: {manager_user.hashed_password}")
        
        # Create a new hash with a shorter password to avoid the 72-byte limit
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password = "manager123"
        
        print(f"Creating hash for password: {password}")
        print(f"Password length: {len(password)}")
        
        # Hash the password
        new_hashed_password = pwd_context.hash(password)
        print(f"New hashed password: {new_hashed_password}")
        
        # Update the user
        manager_user.hashed_password = new_hashed_password
        db.commit()
        
        print("✅ Manager user updated successfully!")
        
        # Verify the password
        print("Verifying password...")
        is_valid = pwd_context.verify(password, new_hashed_password)
        print(f"Password verification result: {is_valid}")
        
        db.close()
        
    except Exception as e:
        print(f"Error creating new hash: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_new_hash()