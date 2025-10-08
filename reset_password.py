#!/usr/bin/env python3
"""
Script to reset user password for testing
"""

import os
import sys
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

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

def reset_password():
    """Reset password for cashier user"""
    db = None
    try:
        # Import required modules
        from app.database import engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        from passlib.context import CryptContext
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Find the cashier user
        user = db.query(User).filter(User.username == 'cashier').first()
        if not user:
            print("Cashier user not found")
            return
            
        # Hash the new password with truncation
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        new_password = 'admin123'
        truncated_password = truncate_password_for_bcrypt(new_password)
        hashed_password = pwd_context.hash(truncated_password)
        
        # Update the password using setattr (like in UserService.update_user)
        setattr(user, 'hashed_password', hashed_password)
        setattr(user, 'updated_at', datetime.utcnow())
        db.commit()
        
        print(f"Password reset successfully for user: {user.username}")
        print(f"New password: {new_password}")
        
    except Exception as e:
        print(f"Error resetting password: {str(e)}")
        if db:
            db.rollback()
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    reset_password()