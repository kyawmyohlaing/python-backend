from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, Token, UserUpdate
    from app.services.user_service import UserService
    from app.models.user import User  # Import the User model
    from app.security import create_access_token, decode_access_token
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from schemas.user_schema import UserCreate, UserResponse, UserLogin, Token, UserUpdate
    from services.user_service import UserService
    from models.user import User  # Import the User model
    from security import create_access_token, decode_access_token

# Change the prefix to match what the frontend expects
router = APIRouter(prefix="/api/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Register
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
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
    # Authenticate user with either email or username
    user = UserService.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}

# Current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID in token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Protected route example
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user

# List all users
@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return UserService.get_users(db)

# Get user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Update user
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = UserService.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Delete user
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None