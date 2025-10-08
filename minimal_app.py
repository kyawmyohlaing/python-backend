import uvicorn
from fastapi import FastAPI, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
try:
    from app.database import get_db, engine, Base
    from app.models.user import User
    from app.services.user_service import UserService
    from app.security import create_access_token
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Minimal FastAPI Backend")

@app.post("/api/auth/login")
def login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        logger.info(f"Login request received for username: {username}")
        # Authenticate user with either email or username
        user = UserService.authenticate_user(db, username, password)
        logger.info(f"User authentication result: {user is not None}")
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        logger.info(f"Creating token for user ID: {user.id}, role: {user.role}")
        # Create token - user.role is already a string
        token = create_access_token({"sub": str(user.id), "role": user.role})
        logger.info(f"Token created successfully")
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Minimal FastAPI Backend"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8088))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "minimal_app:app",
        host=host,
        port=port,
        reload=True,
        log_level="debug"
    )