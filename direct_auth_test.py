#!/usr/bin/env python3
"""
Direct authentication test
"""

import sys
import os

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import engine
    from app.models.user import User
    from app.services.user_service import UserService
except ImportError:
    # Try importing directly (Docker container)
    from database import engine
    from models import User
    from services import UserService

from sqlalchemy.orm import sessionmaker

def direct_auth_test():
    try:
        print("Direct authentication test...")
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test 1: Authenticate with username
        print("\n--- Test 1: Authenticate with username 'manager' ---")
        user1 = UserService.authenticate_user(db, 'manager', 'manager123')
        if user1:
            print(f"✅ Username authentication successful: {user1.username}")
        else:
            print("❌ Username authentication failed")
            
        # Test 2: Authenticate with email
        print("\n--- Test 2: Authenticate with email 'manager@example.com' ---")
        user2 = UserService.authenticate_user(db, 'manager@example.com', 'manager123')
        if user2:
            print(f"✅ Email authentication successful: {user2.username}")
        else:
            print("❌ Email authentication failed")
        
        db.close()
        
    except Exception as e:
        print(f"Error in direct auth test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    direct_auth_test()