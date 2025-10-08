#!/usr/bin/env python3
"""
Manual verification script to test password verification
"""

import sys
import os

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@db:5432/mydb'

def manual_verify():
    """Manually verify the password"""
    try:
        print("Manual password verification...")
        
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
        print(f"Hashed password: {manager_user.hashed_password}")
        
        # Test password verification manually
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password = "manager123"
        
        print(f"Testing password: {password}")
        
        # Verify the password
        is_valid = pwd_context.verify(password, manager_user.hashed_password)
        print(f"Password verification result: {is_valid}")
        
        db.close()
        
    except Exception as e:
        print(f"Error during manual verification: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manual_verify()