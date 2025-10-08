from fastapi import FastAPI, Form, Depends
from sqlalchemy.orm import Session
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

@app.post("/api/auth/login")
def login_user(
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    print(f"Login endpoint called with username: {username}")
    
    # Authenticate user with either email or username
    user = UserService.authenticate_user(db, username, password)
    print(f"User authentication result: {user is not None}")
    
    if not user:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    print(f"Creating token for user ID: {user.id}, role: {user.role}")
    # Fix: Convert enum to string value for JWT token
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    print("Token created successfully")
    
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8089, log_level="debug")