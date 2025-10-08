#!/usr/bin/env python3
"""
Script to update the manager user with a hash created using direct bcrypt
"""

import sys
import os
import bcrypt

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@db:5432/mydb'

def update_with_direct_bcrypt():
    """Update the manager user with a hash created using direct bcrypt"""
    try:
        print("Updating manager user with direct bcrypt hash...")
        
        # Import required modules
        sys.path.append('/app')
        from app.database import engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        
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
        
        # Create a new hash with direct bcrypt
        password = "manager123"
        print(f"Creating hash for password: {password}")
        
        password_bytes = password.encode('utf-8')
        new_hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        print(f"New hashed password: {new_hashed_password}")
        
        # Update the user
        manager_user.hashed_password = new_hashed_password
        db.commit()
        
        print("✅ Manager user updated successfully with direct bcrypt hash!")
        
        # Verify the password
        print("Verifying password...")
        is_valid = bcrypt.checkpw(password_bytes, new_hashed_password.encode('utf-8'))
        print(f"Password verification result: {is_valid}")
        
        db.close()
        
    except Exception as e:
        print(f"Error updating with direct bcrypt: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_with_direct_bcrypt()