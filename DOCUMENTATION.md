# Python Learning Path API - Developer Documentation

This documentation contains the complete chat history and explanations from the AI assistant, organized by topics for beginner developers to learn from.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Backend Structure Creation](#backend-structure-creation)
3. [Database Integration](#database-integration)
4. [Pydantic Schemas Implementation](#pydantic-schemas-implementation)
5. [Clean Separation of Concerns](#clean-separation-of-concerns)
6. [Password Security Implementation](#password-security-implementation)
7. [JWT Authentication Implementation](#jwt-authentication-implementation)
8. [Alembic Migration Setup](#alembic-migration-setup)
9. [Running the Application](#running-the-application)

## Project Overview

A backend API for managing Python learning paths and user progress with database integration.

### Project Structure

```
python_backend_structure/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point of the app
│   ├── database.py          # Database connection and session management
│   ├── config.py            # Configuration settings
│   ├── security.py          # Password hashing and JWT token management
│   ├── dependencies.py      # Dependency injection for authentication
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   └── user_routes.py
│   ├── models/              # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic models (request/response validation)
│   │   ├── __init__.py
│   │   └── user_schema.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── migrations/          # Alembic migrations
│   │   ├── __init__.py
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   └── utils/               # Helper functions
│       ├── __init__.py
│       └── logger.py
│
├── tests/                   # Unit and integration tests
│   └── test_users.py
│
├── requirements.txt         # Python dependencies
├── README.md
└── .env.example             # Example environment variables
```

## Backend Structure Creation

### Initial Setup

The project was created with a modular structure following FastAPI conventions:

1. **App directory** with routes, models, services, config, and utils subdirectories
2. **Tests directory** for unit and integration tests
3. **Requirements.txt** for dependency management
4. **README.md** for project documentation
5. **.env.example** for environment variable examples

### Dependencies Added

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `pytest` - Testing framework
- `httpx` - HTTP client
- `python-dotenv` - Environment variable management

## Database Integration

### Implementation

The backend uses SQLAlchemy ORM with support for both SQLite (for development/testing) and PostgreSQL (for production).

### Key Components

1. **database.py**: Handles database engine creation, session management, and dependency injection
2. **config.py**: Configuration management with environment variable loading
3. **models/user.py**: SQLAlchemy models with proper column definitions

### Configuration

The application supports both SQLite and PostgreSQL. To switch between them, simply change the `DATABASE_URL` in your `.env` file:

#### For SQLite (development):
```
DATABASE_URL=sqlite:///./test.db
```

#### For PostgreSQL (production):
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### Additional Dependencies

- `sqlalchemy` - ORM for database operations
- `psycopg2-binary` - PostgreSQL driver
- `alembic` - Database migrations
- `email-validator` - Email validation for Pydantic schemas
- `passlib` - Password hashing library
- `bcrypt` - bcrypt hashing algorithm
- `python-jose` - JWT token handling
- `cryptography` - Cryptographic operations

## Pydantic Schemas Implementation

### Schema Organization

Created a dedicated `schemas` directory (app/schemas/) with proper file organization for Pydantic models:

1. **UserCreate**: Schema for creating users with name, email, and password
2. **UserRegister**: Schema for user registration
3. **UserLogin**: Schema for user login
4. **Token**: Schema for JWT tokens
5. **TokenData**: Schema for token data
6. **UserUpdate**: Schema for updating users with optional fields
7. **UserResponse**: Schema for API responses with all user fields
8. **ProgressUpdate**: Schema for progress tracking updates

### Benefits

1. **Automatic Validation**: FastAPI automatically validates incoming requests against the Pydantic schemas
2. **Type Safety**: Full type hinting throughout the application
3. **Clean Separation**: Clear distinction between database models and API schemas
4. **Automatic Documentation**: Swagger UI automatically reflects the schema structure
5. **Error Handling**: Automatic error responses for validation failures
6. **Extensibility**: Easy to add new schemas for additional endpoints

## Clean Separation of Concerns

### Database Layer (SQLAlchemy Models)

The SQLAlchemy models in `app/models/user.py` contain only database-related code:

```python
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)  # Hashed password storage
    learning_path = Column(String, nullable=True)
    progress = Column(Text, nullable=True)  # JSON string stored as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### API Layer (Pydantic Schemas)

The Pydantic schemas in `app/schemas/user_schema.py` contain only API-related code:

```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Request for registration
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Response schema (what API returns) - Notice password is not included
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    learning_path: Optional[str] = None
    progress: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # allows SQLAlchemy objects → Pydantic
```

### Benefits of Clean Separation

1. **Independent Evolution**: Database schema and API can evolve independently
2. **Security**: Sensitive fields (like passwords) can be excluded from responses
3. **Flexibility**: Different representations for different API endpoints
4. **Maintainability**: Changes to one layer don't affect the other
5. **Testing**: Each layer can be tested independently
6. **Migration Safety**: Alembic tracks only database models, not API schemas

## Password Security Implementation

### Security Module

The security module in `app/security.py` handles password hashing and verification using bcrypt:

```python
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
```

### Registration and Login Endpoints

#### Registration (`POST /api/v1/users/register`)
- Accepts user credentials (name, email, password)
- Hashes the password before storing in the database
- Returns user information without the password

#### Login (`POST /api/v1/users/login`)
- Accepts email and password
- Verifies the password against the hashed version in the database
- Returns user information if authentication is successful

### How it Works

1. **Register**
   * User sends JSON:
   ```json
   {
     "name": "Kyaw",
     "email": "kyaw@example.com",
     "password": "supersecret123"
   }
   ```
   * Password is hashed before storing in Postgres.

2. **Login**
   * User sends JSON:
   ```json
   {
     "email": "kyaw@example.com",
     "password": "supersecret123"
   }
   ```
   * Password is verified against the hashed version in the DB.
   * If correct → returns user info (without password).

### Benefits

1. **Security**: Passwords are never stored in plain text
2. **Industry Standard**: Uses bcrypt hashing algorithm
3. **Easy to Use**: Simple API endpoints for registration and login
4. **Proper Error Handling**: Returns appropriate HTTP status codes
5. **Validation**: Uses Pydantic schemas for input validation

## JWT Authentication Implementation

### Security Module Extensions

The security module in `app/security.py` now includes JWT token handling:

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# JWT settings
SECRET_KEY = "your-secret-key"  # put a strong random key in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

# JWT functions
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### Dependencies Module

The dependencies module in `app/dependencies.py` handles JWT token validation:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.security import decode_access_token

# OAuth2 scheme for JWT token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
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
```

### Authentication Endpoints

#### Login (`POST /api/v1/users/login`)
- Accepts email and password
- Verifies credentials
- Returns JWT token instead of user object

#### Get Current User (`GET /api/v1/users/me`)
- Protected endpoint that requires valid JWT token
- Returns authenticated user information

### How it Works

1. **Login**
   * User sends credentials:
   ```json
   {
     "email": "john@example.com",
     "password": "securepassword"
   }
   ```
   * System verifies credentials
   * If valid, returns JWT token:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

2. **Access Protected Routes**
   * Client includes token in Authorization header:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
   * Server validates token and grants access

### Benefits

1. **Stateless Authentication**: No server-side session storage
2. **Industry Standard**: Uses JWT tokens for authentication
3. **Secure**: Tokens are signed and can expire
4. **Scalable**: Works well in distributed systems
5. **Standard Implementation**: Follows OAuth2 Bearer Token standard

## Alembic Migration Setup

### Restructured Organization

Alembic was restructured to be inside the `app/` folder for cleaner organization:

```
app/
└── migrations/
    ├── __init__.py
    ├── alembic.ini
    ├── env.py
    ├── script.py.mako
    └── versions/
```

### Configuration Files

#### alembic.ini
- Configured to work within the app package structure
- Left `sqlalchemy.url` blank to load from config.py
- Set `script_location = app/migrations` to point to the correct location

#### env.py
- Added proper path configuration to include the app folder
- Imported all models to ensure they are registered with Base
- Configured both offline and online migration modes

### Usage Instructions

1. **Create a New Migration**:
   ```bash
   alembic -c app/migrations/alembic.ini revision --autogenerate -m "description of changes"
   ```

2. **Apply Migrations**:
   ```bash
   alembic -c app/migrations/alembic.ini upgrade head
   ```

3. **Downgrade Migrations**:
   ```bash
   alembic -c app/migrations/alembic.ini downgrade -1
   ```

## Running the Application

### Setup Process

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```env
   ENVIRONMENT=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///./test.db  # or postgresql://user:password@localhost:5432/dbname
   ```

### Starting the Server

To run the application in development mode:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## API Endpoints

All endpoints are prefixed with `/api/v1/users`:

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Authenticate user and return JWT token
- `GET /me` - Get current authenticated user

### User Management
- `POST /` - Create a new user
- `GET /{user_id}` - Get a user by ID
- `PUT /{user_id}` - Update a user
- `DELETE /{user_id}` - Delete a user
- `GET /` - List all users

### Progress Tracking
- `POST /{user_id}/progress` - Update user progress on a module

## Request/Response Format

### Register User (POST /register)
Request body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "learning_path": null,
  "progress": {},
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Login User (POST /login)
Request body:
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User (GET /me)
Request header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "learning_path": null,
  "progress": {},
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Update Progress (POST /{user_id}/progress)
Request body:
```json
{
  "module_id": "python-basics",
  "completed": true
}
```

## Testing

To run tests:

```bash
pytest
```

## Learning Path for Beginners

### 1. Understanding the Structure
- Start by exploring the directory structure
- Understand the separation of concerns (routes, models, services, schemas)
- Learn how each component interacts with others

### 2. Database Integration
- Learn SQLAlchemy basics
- Understand ORM concepts
- Practice creating models and relationships

### 3. API Development
- Learn FastAPI basics
- Understand request/response validation with Pydantic
- Practice creating endpoints with proper error handling

### 4. Security Implementation
- Learn password hashing with bcrypt
- Understand authentication concepts
- Practice implementing secure registration and login
- Learn JWT token-based authentication

### 5. Database Migrations
- Learn Alembic basics
- Understand migration workflows
- Practice creating and applying migrations

### 6. Testing
- Learn pytest basics
- Understand unit and integration testing
- Practice writing tests for API endpoints

### 7. Deployment
- Learn environment configuration
- Understand production deployment considerations
- Practice deploying to different environments

## Best Practices Followed

1. **Separation of Concerns**: Clear distinction between routes, services, models, and schemas
2. **Type Safety**: Full type hinting throughout the application
3. **Automatic Validation**: Request/response validation with Pydantic
4. **Database Migrations**: Safe schema changes with Alembic
5. **Environment Configuration**: Proper environment variable management
6. **Documentation**: Comprehensive documentation for all components
7. **Testing**: Unit and integration tests for all functionality
8. **Clean Architecture**: Database layer (SQLAlchemy) separated from API layer (Pydantic)
9. **Security**: Password hashing with bcrypt, exclusion of sensitive data from responses
10. **Authentication**: JWT token-based authentication following industry standards

## Common Issues and Solutions

### 1. uvicorn command not found
- Ensure virtual environment is activated
- Install dependencies with `pip install -r requirements.txt`

### 2. Database connection issues
- Check DATABASE_URL in .env file
- Ensure database server is running
- Verify credentials are correct

### 3. Migration errors
- Ensure all models are imported in env.py
- Check migration file syntax
- Verify database permissions

### 4. Password verification issues
- Ensure passlib and bcrypt are installed
- Check that passwords are properly hashed during registration
- Verify that the verify_password function is correctly implemented

### 5. JWT token issues
- Ensure SECRET_KEY is properly configured
- Check token expiration settings
- Verify token validation logic in dependencies

## Next Steps for Learning

1. Add refresh token functionality
2. Implement role-based access control
3. Add password reset functionality
4. Implement more complex relationships between models
5. Add caching with Redis
6. Implement background tasks
7. Add logging and monitoring
8. Deploy to a cloud platform
9. Add more comprehensive testing
10. Implement CI/CD pipeline

This documentation serves as a comprehensive guide for beginner developers to understand the complete development process, from initial structure creation to advanced features like database migrations, password security, and JWT authentication.