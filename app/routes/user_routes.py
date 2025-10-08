from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, Token, UserUpdate
    from app.services.user_service import UserService
    from app.models.user import User  # Import the User model
    from app.security import create_access_token, decode_access_token
    from app.dependencies import get_current_user  # Use shared dependency
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from schemas.user_schema import UserCreate, UserResponse, UserLogin, Token, UserUpdate
    from services.user_service import UserService
    from models.user import User  # Import the User model
    from security import create_access_token, decode_access_token
    from dependencies import get_current_user  # Use shared dependency

# Change the prefix to match what the frontend expects
router = APIRouter(prefix="/api/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Register
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("Register user endpoint called")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return UserService.create_user(db, user)

# Login - Updated to accept form data
@router.post("/login", response_model=Token)
def login_user(
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Login endpoint called with username: {username}")
    try:
        # Log the received form data
        logger.info(f"Received form data - username: {username}, password: {'*' * len(password)}")
        
        # Authenticate user with either email or username
        user = UserService.authenticate_user(db, username, password)
        logger.info(f"User authentication result: {user is not None}")
        
        if not user:
            logger.warning(f"Authentication failed for user: {username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
        logger.info(f"Creating token for user ID: {user.id}, role: {user.role}")
        # Fix: Convert enum to string value for JWT token
        token = create_access_token({"sub": str(user.id), "role": user.role.value})
        logger.info("Token created successfully")
        
        response_data = {"access_token": token, "token_type": "bearer"}
        logger.info(f"Sending response: {response_data}")
        return response_data
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in login_user: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# Remove the duplicate get_current_user function - using the shared one from dependencies.py

# Protected route example
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user

# List all users (protected)
@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserService.get_users(db)

# Get user by ID (protected)
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Update user (protected)
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = UserService.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Delete user (protected)
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None