from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import json
import logging

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.models.user import User, UserRole
    from app.schemas.user_schema import UserCreate, UserUpdate
    from app.security import hash_password, verify_password
except ImportError:
    # Try importing directly (Docker container)
    from models.user import User, UserRole
    from schemas.user_schema import UserCreate, UserUpdate
    from security import hash_password, verify_password

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        logger.info(f"Creating user with email: {user.email}")
        try:
            # Hash the password
            hashed_password = hash_password(user.password)
            
            # Create default progress JSON
            progress_json = json.dumps({
                "modules": {},
                "current_module": None,
                "completed": False
            })
            
            # Create the user object with the correct field names
            db_user = User(
                username=user.username,  # Fixed: use username instead of name to match schema
                email=user.email,
                hashed_password=hashed_password,
                progress=progress_json,
                role=user.role
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User created successfully with ID: {db_user.id}")
            return db_user
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error during user creation: {str(e)}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error during user creation: {str(e)}")
            raise

    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
        
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
            
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
            
        db.delete(db_user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, identifier: str, password: str):
        """
        Authenticate user with either email or username
        """
        # Try to find user by email first
        user = UserService.get_user_by_email(db, identifier)
        
        # If not found by email, try to find by username
        if not user:
            user = UserService.get_user_by_username(db, identifier)
            
        # If user not found or password doesn't match, return None
        if not user or not verify_password(password, str(user.hashed_password)):
            return None
            
        return user