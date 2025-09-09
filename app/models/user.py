from sqlalchemy import Column, Integer, String
# Since we're in the container and files are directly in /app, we import directly
from database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    learning_path = Column(String, nullable=True)
    progress = Column(String, nullable=True)  # Store as JSON string

# Pydantic models for API validation
class UserBase(BaseModel):
    """Base user model with common attributes"""
    name: str
    email: str
    learning_path: Optional[str] = None

class UserCreate(UserBase):
    """Model for creating a new user"""
    # Note: In a real application, we would not include password in plain text
    # This is just for demonstration purposes
    password: str

class UserUpdate(BaseModel):
    """Model for updating user information"""
    name: Optional[str] = None
    email: Optional[str] = None
    learning_path: Optional[str] = None
    progress: Optional[dict] = None

class UserResponse(UserBase):
    """Response model for user data"""
    id: int
    progress: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True