from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
import sys
import os

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
    import traceback
    traceback.print_exc()
    sys.exit(1)

app = FastAPI()

@app.post("/test-login")
def test_login(username: str = Form(...), password: str = Form(...)):
    try:
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        print(f"Login endpoint called with username: {username}")
        
        # Authenticate user with either email or username
        user = UserService.authenticate_user(db, username, password)
        print(f"User authentication result: {user is not None}")
        
        if not user:
            return {"error": "Invalid credentials"}
            
        print(f"Creating token for user ID: {user.id}, role: {user.role}")
        # Fix: Convert enum to string for JWT token
        token = create_access_token({"sub": str(user.id), "role": str(user.role)})
        print("Token created successfully")
        
        # Close database session
        try:
            next(db_gen)
        except StopIteration:
            pass
        
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error in login_user: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

client = TestClient(app)

def test_login_endpoint():
    response = client.post("/test-login", data={"username": "manager", "password": "manager123"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_login_endpoint()