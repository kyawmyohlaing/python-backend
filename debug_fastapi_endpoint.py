import sys
import os
import traceback

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules
try:
    from app.database import get_db
    from app.services.user_service import UserService
    from app.security import create_access_token
    print("Successfully imported modules")
except ImportError as e:
    print(f"Import error: {e}")
    traceback.print_exc()
    sys.exit(1)

def test_fastapi_login_endpoint():
    print("Testing FastAPI login endpoint logic...")
    
    try:
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        print("Database session created")
        
        # Simulate the login endpoint logic
        username = "manager"
        password = "manager123"
        
        print(f"Login endpoint called with username: {username}")
        
        # Authenticate user with either email or username
        user = UserService.authenticate_user(db, username, password)
        print(f"User authentication result: {user is not None}")
        
        if not user:
            print("Invalid credentials")
            return
            
        print(f"Creating token for user ID: {user.id}, role: {user.role}")
        # Fix: user.role is already a string, no need to access .value
        token = create_access_token({"sub": str(user.id), "role": user.role})
        print("Token created successfully")
        print(f"Token: {token}")
        
        # Return the response that the FastAPI endpoint would return
        response = {"access_token": token, "token_type": "bearer"}
        print(f"Response: {response}")
        
        # Close database session
        try:
            next(db_gen)
        except StopIteration:
            pass
            
    except Exception as e:
        print(f"Error in login endpoint logic: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_fastapi_login_endpoint()