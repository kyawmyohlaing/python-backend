#!/usr/bin/env python3
"""
Script to fix the manager user's password - designed to run inside Docker container
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append('/app')

def fix_manager_password():
    """Fix the manager user's password"""
    try:
        print("Fixing manager user's password...")
        
        # Import required modules
        from app.database import engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        from app.security import hash_password
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Find the manager user
        manager_user = db.query(User).filter(User.username == 'manager').first()
        
        if not manager_user:
            print("Manager user not found!")
            return
            
        print(f"Found manager user: {manager_user.username}")
        
        # Hash the new password with proper truncation (using our security module)
        new_password = "manager123"
        new_hashed_password = hash_password(new_password)
        
        print(f"New password hash: {new_hashed_password}")
        
        # Update the manager user's password
        manager_user.hashed_password = new_hashed_password
        db.commit()
        
        print("✅ Manager user's password updated successfully!")
        print(f"New password: {new_password}")
        
        db.close()
        
    except Exception as e:
        print(f"Error fixing manager password: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_manager_password()