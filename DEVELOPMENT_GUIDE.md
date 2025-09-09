# FastAPI Backend Template Development Guide

This guide provides detailed information for developers working on the FastAPI backend template.

## 🏗️ Project Architecture

The project follows a clean architecture pattern with clear separation of concerns:

```
app/
├── main.py              # Application entry point
├── config.py            # Configuration management
├── database.py          # Database connection and session management
├── security.py          # Authentication and password hashing
├── models/              # Database models (SQLAlchemy)
├── schemas/             # Data validation models (Pydantic)
├── services/            # Business logic
├── routes/              # API endpoints
└── migrations/          # Database migrations (Alembic)
```

## 🧱 Core Components

### Main Application (`app/main.py`)

- Creates the FastAPI application instance
- Includes all route modules
- Handles startup and shutdown events

### Configuration (`app/config.py`)

- Loads environment variables using python-dotenv
- Provides centralized configuration management

### Database (`app/database.py`)

- Sets up SQLAlchemy engine and session
- Provides database session dependency for routes

### Security (`app/security.py`)

- Implements password hashing with bcrypt
- Handles JWT token creation and validation
- Provides authentication utilities

### Models (`app/models/`)

- Define database schema using SQLAlchemy
- Each model represents a database table

### Schemas (`app/schemas/`)

- Define data validation using Pydantic
- Separate schemas for input, output, and internal use

### Services (`app/services/`)

- Contain business logic
- Interact with database models
- Handle data processing and transformation

### Routes (`app/routes/`)

- Define API endpoints
- Handle HTTP requests and responses
- Use services to process data

## 🐳 Docker Configuration

### Dockerfile

- Uses Python 3.11 slim image
- Installs dependencies from requirements.txt
- Copies application code
- Uses Gunicorn with Uvicorn workers for production

### docker-compose.yml

- Defines production services
- Configures PostgreSQL database
- Sets up environment variables

### docker-compose.override.yml

- Overrides production configuration for development
- Enables hot reload with volume mounting
- Uses Uvicorn directly for development

## 🗃️ Database Migrations

### Alembic Setup

- Migrations are stored in `app/migrations/versions/`
- Environment configuration in `app/migrations/env.py`
- Migration script template in `app/migrations/script.py.mako`

### Creating Migrations

```bash
# Generate a new migration
docker-compose exec web alembic -c app/migrations/alembic.ini revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head
```

### Seeding Data

- Create migration files that insert initial data
- Use revision dependencies to ensure proper order

## 🔐 Authentication Flow

1. User registers with email and password
2. Password is hashed using bcrypt
3. User logs in with email and password
4. Password is verified against hashed version
5. JWT token is generated and returned
6. Client includes token in Authorization header
7. Server validates token and extracts user information

## 🧪 Testing

### Unit Tests

- Located in `tests/` directory
- Test individual functions and components
- Use pytest framework

### Integration Tests

- Test API endpoints
- Use TestClient from FastAPI
- Test database interactions

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
python -m pytest tests/test_users.py

# Run with coverage
python -m pytest --cov=app tests/
```

## 🛠️ Development Workflow

### Adding New Features

1. Create new model in `app/models/`
2. Create corresponding schema in `app/schemas/`
3. Implement service logic in `app/services/`
4. Add API endpoints in `app/routes/`
5. Create database migration
6. Add tests
7. Update documentation

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### Dependencies

- Add new dependencies to `requirements.txt`
- Pin versions for production dependencies
- Use extras for optional dependencies

## 📦 Project Structure Details

### Models (`app/models/user.py`)

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
```

### Schemas (`app/schemas/user_schema.py`)

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    
    class Config:
        orm_mode = True
```

### Services (`app/services/user_service.py`)

```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.security import hash_password

def create_user(db: Session, user_data: UserCreate):
    hashed_pw = hash_password(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

### Routes (`app/routes/user_routes.py`)

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)
```

## 🚀 Deployment

### Environment Variables

For production deployment, ensure these environment variables are set:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Scaling

- Adjust Gunicorn worker count in Dockerfile
- Use a reverse proxy like Nginx
- Consider using a managed database service
- Implement caching where appropriate

## 🛡️ Security Best Practices

1. Never store passwords in plain text
2. Use environment variables for secrets
3. Validate all input data
4. Implement proper error handling
5. Use HTTPS in production
6. Regularly update dependencies
7. Implement rate limiting for public endpoints
8. Use Content Security Policy headers

## 📊 Monitoring and Logging

### Logging

- Use Python's built-in logging module
- Configure different log levels for development and production
- Log important events and errors

### Monitoring

- Monitor application health endpoints
- Track database performance
- Monitor resource usage (CPU, memory, disk)
- Set up alerts for critical issues

## 🤝 Contributing

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

### Code Review Guidelines

- Review code for security issues
- Check for proper error handling
- Ensure tests are comprehensive
- Verify documentation is up to date
- Check for performance issues

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Logging Guide](https://docs.python.org/3/howto/logging.html)

## 🐛 Handling Type Checking Issues

### Common Type Errors with SQLAlchemy Models

When working with SQLAlchemy models, you may encounter type checking errors where the type checker interprets a model attribute as the Column definition rather than the actual value. This commonly occurs in scenarios like:

```python
# This may cause type errors with some checkers
progress = json.loads(db_user.progress) if db_user.progress else {}
```

### Solutions

1. **Use getattr() for explicit attribute access:**
   ```python
   progress_str = getattr(db_user, 'progress', None)
   progress = json.loads(progress_str) if progress_str else {}
   ```

2. **Add type ignore comments when necessary:**
   ```python
   db_user.progress = json.dumps(progress)  # type: ignore
   ```

3. **Use type casting when appropriate:**
   ```python
   from typing import cast
   progress_str = cast(str, db_user.progress)
   progress = json.loads(progress_str) if progress_str else {}
   ```

These approaches help ensure that both static analysis tools and runtime behavior work correctly with your code.
