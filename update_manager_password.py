#!/usr/bin/env python3
"""
Script to properly update the manager user's password in the PostgreSQL database
"""

import sys
import os
from datetime import datetime

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@db:5432/mydb'

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

def update_manager_password():
    """Update the manager user's password with a proper bcrypt hash"""
    try:
        print("Updating manager user's password...")

        # Import required modules
        sys.path.append('/app')
        from app.database import engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        from passlib.context import CryptContext

        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Find the manager user
        manager_user = db.query(User).filter(User.username == 'manager').first()
        
        if not manager_user:
            print("Manager user not found!")
            return

        print(f"Found manager user: {manager_user.username}")
        print(f"Current password hash: {manager_user.hashed_password}")

        # Hash the password with proper bcrypt and truncation
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        new_password = "manager123"
        truncated_password = truncate_password_for_bcrypt(new_password)
        new_hashed_password = pwd_context.hash(truncated_password)
        
        print(f"New password hash: {new_hashed_password}")

        # Update the manager user's password using setattr (like in other scripts)
        setattr(manager_user, 'hashed_password', new_hashed_password)
        setattr(manager_user, 'updated_at', datetime.utcnow())
        db.commit()

        print("✅ Manager user's password updated successfully!")
        print(f"New password: {new_password}")

        # Verify the update
        updated_user = db.query(User).filter(User.username == 'manager').first()
        if updated_user:
            print(f"Verified hash: {updated_user.hashed_password}")

        db.close()

    except Exception as e:
        print(f"Error updating manager password: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_manager_password()