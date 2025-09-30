from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.user import User, UserRole
    from app.security import decode_access_token
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.user import User, UserRole
    from security import decode_access_token

# OAuth2 scheme for JWT token - Updated to match the actual login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get the current user from the JWT token.
    
    Args:
        token (str): JWT token from the Authorization header
        db (Session): Database session
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extract user ID from token
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
        
    return user

def require_role(required_role: UserRole):
    """
    Dependency to check if the current user has the required role.
    
    Args:
        required_role (UserRole): The role required to access the endpoint
        
    Returns:
        function: A dependency function that validates the user's role
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        # Compare role values as strings
        if str(current_user.role) != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role.value}"
            )
        return current_user
    return role_checker

def require_any_role(required_roles: list[UserRole]):
    """
    Dependency to check if the current user has any of the required roles.
    
    Args:
        required_roles (list[UserRole]): List of roles that can access the endpoint
        
    Returns:
        function: A dependency function that validates the user's role
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        # Get role values as strings for comparison
        role_values = [role.value for role in required_roles]
        if str(current_user.role) not in role_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {role_values}"
            )
        return current_user
    return role_checker