#!/usr/bin/env python3
"""
Test login function directly
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
try:
    from app.database import engine, get_db
    from app.routes.user_routes import login_user
    from sqlalchemy.orm import sessionmaker
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def test_login_function():
    try:
        print("Testing login function directly...")
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test the login function directly
        print("Calling login_user function with username='manager', password='manager123'")
        result = login_user("manager", "manager123", db)
        print(f"Login function result: {result}")
        
        db.close()
        
    except Exception as e:
        print(f"Error testing login function: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login_function()