#!/usr/bin/env python3
"""
Script to test authentication with manager user
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_auth():
    """Test authentication with manager user"""
    try:
        # Import required modules
        from app.database import engine, get_db
        from app.models.user import User
        from app.services.user_service import UserService
        from sqlalchemy.orm import sessionmaker
        
        print("Testing authentication with manager user...")
        
        # Test with database session
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Test authentication
            print("Attempting to authenticate manager user...")
            user = UserService.authenticate_user(db, "manager", "manager123")
            
            if user:
                print(f"✅ Authentication successful!")
                print(f"User ID: {user.id}")
                print(f"Username: {user.username}")
                print(f"Role: {user.role}")
            else:
                print("❌ Authentication failed")
                
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # Close the database session
            try:
                db_gen.close()
            except:
                pass
        
    except Exception as e:
        print(f"Error in test_auth: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auth()