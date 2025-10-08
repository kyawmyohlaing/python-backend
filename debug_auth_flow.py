import sqlite3
import os
import sys
import traceback

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules
try:
    from app.database import get_db
    from app.services.user_service import UserService
    from app.models.user import User
    print("Successfully imported modules")
except ImportError as e:
    print(f"Import error: {e}")
    traceback.print_exc()
    sys.exit(1)

def test_auth_flow():
    print("Testing authentication flow...")
    
    try:
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        print("Database session created")
        
        # Test user lookup by username
        print("\n1. Looking up manager user by username...")
        user = UserService.get_user_by_username(db, "manager")
        if user:
            print(f"User found: {user.username}, {user.email}, {user.role}")
        else:
            print("User not found by username")
            return
            
        # Test user lookup by email
        print("\n2. Looking up manager user by email...")
        user_by_email = UserService.get_user_by_email(db, "manager@example.com")
        if user_by_email:
            print(f"User found by email: {user_by_email.username}, {user_by_email.email}, {user_by_email.role}")
        else:
            print("User not found by email")
            
        # Test authentication
        print("\n3. Testing authentication...")
        authenticated_user = UserService.authenticate_user(db, "manager", "manager123")
        if authenticated_user:
            print(f"Authentication successful: {authenticated_user.username}, {authenticated_user.email}, {authenticated_user.role}")
        else:
            print("Authentication failed")
            
        # Test authentication with email
        print("\n4. Testing authentication with email...")
        authenticated_user_email = UserService.authenticate_user(db, "manager@example.com", "manager123")
        if authenticated_user_email:
            print(f"Authentication with email successful: {authenticated_user_email.username}, {authenticated_user_email.email}, {authenticated_user_email.role}")
        else:
            print("Authentication with email failed")
            
        # Close database session
        try:
            next(db_gen)
        except StopIteration:
            pass
            
    except Exception as e:
        print(f"Error during authentication flow test: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_flow()