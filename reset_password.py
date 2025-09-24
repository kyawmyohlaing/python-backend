#!/usr/bin/env python3
"""
Script to reset user password for testing
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def reset_password():
    """Reset password for cashier user"""
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
            
        # Hash the new password
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        new_password = 'admin123'
        hashed_password = pwd_context.hash(new_password)
        
        # Update the password
        user.hashed_password = hashed_password
        db.commit()
        
        print(f"Password reset successfully for user: {user.username}")
        print(f"New password: {new_password}")
        
    except Exception as e:
        print(f"Error resetting password: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    reset_password()