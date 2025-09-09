# Changelog

All notable changes to the FastAPI Backend Template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation files
- Setup guide
- API documentation
- Development guide
- Troubleshooting guide
- FAQ
- Changelog
- Documentation for type checking issues in UserService

### Changed
- Improved README.md with better structure and information
- Enhanced Makefile with additional commands
- Updated Docker configuration for better performance

### Fixed
- Minor issues in example files
- Documentation inconsistencies
- Type checking issue in UserService.update_user_progress method where Column[str] was being passed to json.loads instead of the actual string value

## [1.0.0] - 2025-09-05

### Added
- Initial release of the FastAPI Backend Template
- FastAPI application with user management
- PostgreSQL database integration
- SQLAlchemy ORM models
- Pydantic schemas for data validation
- User service with business logic
- User routes for registration, login, and profile
- JWT-based authentication
- Password hashing with bcrypt
- Alembic database migrations
- Docker configuration for development and production
- Docker Compose setup with PostgreSQL
- Environment variable management
- Example user seeding
- Unit and integration tests
- Makefile for common tasks
- Comprehensive README with setup instructions
- Requirements.txt with all dependencies
- .env.example for environment configuration
- .gitignore for version control
- LICENSE file
- Project summary documentation

### Features
- User registration with email uniqueness validation
- User login with JWT token generation
- Protected routes requiring authentication
- User profile retrieval
- Automatic database migrations on startup
- Development mode with hot reload
- Production mode with Gunicorn workers
- Seeded example user for immediate testing
- Comprehensive test suite
- Docker containerization
- Environment-based configuration

### Security
- Password hashing with Bcrypt
- JWT token-based authentication
- Secure password storage (never store plain text passwords)
- Protected routes with token verification
- Environment variable-based secret management

### Documentation
- README with quick start guide
- Project structure overview
- Makefile command reference
- Authentication flow explanation
- API endpoint testing examples
- Project summary

### Testing
- Unit tests for user service functions
- Integration tests for API endpoints
- Both SQLite (in-memory) and PostgreSQL testing support
- Test runner script for easy execution

### Dependencies
- fastapi
- uvicorn
- gunicorn
- sqlalchemy
- psycopg2-binary
- alembic
- python-dotenv
- passlib[bcrypt]
- python-jose[cryptography]
- pydantic
- email-validator
- pytest
- httpx

### Docker Configuration
- Production Dockerfile with Gunicorn and Uvicorn workers
- docker-compose.yml for production services configuration
- docker-compose.override.yml for development environment overrides
- Multi-stage deployment supporting both development and production environments
- Automatic migration execution on startup
- Volume mounting for development hot reload

### Project Structure
```
fastapi-backend-template/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user_schema.py
│   ├── services/
│   │   └── user_service.py
│   ├── routes/
│   │   └── user_routes.py
│   └── migrations/
│       ├── alembic.ini
│       ├── env.py
│       └── versions/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── start.sh
├── Makefile
├── requirements.txt
└── .env.example
```

## [0.1.0] - 2025-09-04

### Added
- Initial project structure
- Basic FastAPI application
- User model and schema
- User service and routes
- Basic authentication
- Docker configuration
- Requirements file
- README file

[Unreleased]: https://github.com/your-username/fastapi-backend-template/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/your-username/fastapi-backend-template/releases/tag/v1.0.0
[0.1.0]: https://github.com/your-username/fastapi-backend-template/releases/tag/v0.1.0