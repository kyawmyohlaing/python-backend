from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import cast

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.config import Config
except ImportError:
    # Try importing directly (Docker container)
    from config import Config

# Get config instance
config = Config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

# Maximum password length for bcrypt (72 bytes)
MAX_PASSWORD_LENGTH = 72

def truncate_password_for_bcrypt(password: str) -> str:
    """
    Truncate password to 72 bytes for bcrypt compatibility.
    Bcrypt has a limitation where only the first 72 bytes are used.
    """
    if isinstance(password, str):
        # Encode to bytes to check actual byte length
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > MAX_PASSWORD_LENGTH:
            # Truncate to 72 bytes and decode back to string
            truncated_bytes = password_bytes[:MAX_PASSWORD_LENGTH]
            return truncated_bytes.decode('utf-8', errors='ignore')
    return password

# Password hashing
def hash_password(password: str) -> str:
    # Truncate password if it's too long for bcrypt
    truncated_password = truncate_password_for_bcrypt(password)
    return pwd_context.hash(truncated_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password if it's too long for bcrypt
    truncated_password = truncate_password_for_bcrypt(plain_password)
    return pwd_context.verify(truncated_password, hashed_password)

# JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    # Cast SECRET_KEY to str since it's validated in config.py
    secret_key = cast(str, config.SECRET_KEY)
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        # Cast SECRET_KEY to str since it's validated in config.py
        secret_key = cast(str, config.SECRET_KEY)
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None