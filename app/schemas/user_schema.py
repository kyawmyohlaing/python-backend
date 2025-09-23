from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.models.user import UserRole
except ImportError:
    # Try importing directly (Docker container)
    from models.user import UserRole

class UserCreate(BaseModel):
    username: str  # Changed from name to username to match model
    email: EmailStr
    password: str
    role: UserRole = UserRole.WAITER  # Default role

class UserResponse(BaseModel):
    id: int
    username: str  # Changed from name to username to match model
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    # Accept either email or username for login
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str
    
    # Ensure either email or username is provided
    def validate_login_fields(self):
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided")
        return self

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None)  # Changed from name to username to match model
    email: Optional[EmailStr] = Field(default=None)
    role: Optional[UserRole] = Field(default=None)

class ProgressUpdate(BaseModel):
    module_id: str
    completed: bool