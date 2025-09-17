import json
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.models.user import User
    from app.schemas.user_schema import UserCreate, UserUpdate
    from app.security import hash_password, verify_password
except ImportError:
    # Try importing directly (Docker container)
    from models.user import User
    from schemas.user_schema import UserCreate, UserUpdate
    from security import hash_password, verify_password

class UserService:
    """Service class for handling user-related business logic"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user with generated ID and timestamps"""
        # Hash the password before storing
        hashed_password = hash_password(user_data.password)
        
        # Initialize progress as empty JSON string
        progress_json = json.dumps({})
        
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            learning_path=getattr(user_data, 'learning_path', None),
            progress=progress_json
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, str(user.password)):
            return user
        return None
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """Get a user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get a user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
            
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Handle progress field conversion
        if 'progress' in update_data:
            update_data['progress'] = json.dumps(update_data['progress'])
            
        for field, value in update_data.items():
            setattr(db_user, field, value)
            
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user by ID"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
            
        db.delete(db_user)
        db.commit()
        return True
    
    @staticmethod
    def update_user_progress(db: Session, user_id: int, module_id: str, completed: bool) -> Optional[User]:
        """Update user's progress on a specific module"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
            
        # Parse existing progress or create new
        try:
            # Ensure we're working with the actual value, not the column object
            progress_str = getattr(db_user, 'progress', None)
            progress = json.loads(progress_str) if progress_str else {}
        except (json.JSONDecodeError, TypeError):
            progress = {}
        
        # Update progress
        progress[module_id] = {
            "completed": completed,
            "updated_at": datetime.now().isoformat()
        }
        
        # Save back as JSON string
        db_user.progress = json.dumps(progress)  # type: ignore
        db.commit()
        db.refresh(db_user)
        return db_user