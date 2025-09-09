# FastAPI Backend Template

A production-ready, scalable FastAPI backend template with PostgreSQL, Alembic migrations, JWT authentication, and Docker support. This template provides a solid foundation for building secure, high-performance web APIs with Python.

## 🌟 Key Features

- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints
- **PostgreSQL**: Production-ready relational database with persistent storage
- **SQLAlchemy**: High-performance SQL toolkit and Object-Relational Mapping (ORM) library
- **Alembic**: Lightweight database migration tool with automatic seeding capabilities
- **JWT Authentication**: Secure token-based authentication using JSON Web Tokens
- **Bcrypt**: Industry-standard password hashing for enhanced security
- **Pydantic**: Data validation and settings management using Python type annotations
- **Docker**: Containerization for consistent development, testing, and production environments
- **Gunicorn**: Production-ready Python WSGI HTTP Server
- **Hot Reload**: Development mode with automatic reloading for rapid iteration
- **Environment Configuration**: Flexible configuration management with .env files
- **Comprehensive Testing**: Unit and integration tests with pytest

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd fastapi-backend-template

# Copy the environment file and configure your settings
cp .env.example .env
# Edit .env file with your configuration

# Start in development mode (with hot reload)
make dev

# Or start in production mode (with Gunicorn workers)
make prod
```

The application will be available at `http://localhost:8088`.

## 📁 Project Structure

```
fastapi-backend-template/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection setup
│   ├── security.py          # Security utilities (hashing, JWT)
│   ├── dependencies.py      # FastAPI dependencies
│   ├── models/              # Database models
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas for validation
│   │   └── user_schema.py
│   ├── services/            # Business logic layer
│   │   └── user_service.py
│   ├── routes/              # API endpoints
│   │   └── user_routes.py
│   ├── utils/               # Utility functions
│   │   └── logger.py
│   └── migrations/          # Database migrations
│       ├── alembic.ini
│       ├── env.py
│       └── versions/
├── tests/                   # Test suite
│   ├── conftest.py
│   ├── test_users.py
│   └── test_users_postgres.py
├── Dockerfile               # Application container definition
├── docker-compose.yml       # Production services definition
├── docker-compose.override.yml  # Development services override
├── start.sh                 # Application entrypoint script
├── entrypoint.sh            # Migration entrypoint script
├── Makefile                 # Common commands and workflows
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── TROUBLESHOOTING_DOCKER.md # Docker troubleshooting guide
└── README.md                # This file
```

## 🛠️ Development Workflow

### Makefile Commands

```bash
make dev       # Start development environment (hot reload)
make prod      # Start production environment (Gunicorn)
make down      # Stop all containers
make logs      # View application logs
make migrate   # Run database migrations
make test      # Run test suite
make backup    # Create a database backup
make clean     # Remove Docker containers, networks, and volumes
make setup     # Setup environment (copy .env.example to .env)
```

### Environment Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Configure your environment variables in the `.env` file:
   - `SECRET_KEY`: Cryptographically secure key for JWT signing (required)
   - `DATABASE_URL`: PostgreSQL connection string
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time

### Database Migrations

The template uses Alembic for database migrations:

```bash
# Generate a new migration
alembic -c app/migrations/alembic.ini revision --autogenerate -m "Migration message"

# Apply migrations
make migrate

# Or run directly
alembic -c app/migrations/alembic.ini upgrade head
```

## 🔐 Authentication

The template includes JWT-based authentication with the following endpoints:

- `POST /users/register` - Register a new user
- `POST /users/login` - Login and receive a JWT token
- `GET /users/me` - Get current user (JWT protected)

### Seeded Example User

The database is automatically seeded with an example user for testing:

- Email: `user@example.com`
- Password: `password123`

### Testing with cURL

```bash
# Register a new user
curl -X POST http://localhost:8088/users/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "securepassword"}'

# Login with the example user
curl -X POST http://localhost:8088/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Access protected route (replace <access_token> with the token from the login response)
curl http://localhost:8088/users/me \
  -H "Authorization: Bearer <access_token>"
```

## 🐳 Docker Configuration

The template includes a complete Docker setup with separate configurations for development and production:

- **Development**: Uses Uvicorn with hot reload for rapid development
- **Production**: Uses Gunicorn with multiple workers for high performance
- **PostgreSQL**: Persistent database storage with volume mapping
- **Automatic Migrations**: Alembic migrations run automatically on startup

### Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## 🧪 Testing

The template includes a comprehensive test suite using pytest:

```bash
# Run unit tests
make test

# Or run directly
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### Test Configuration

- Tests use an in-memory SQLite database by default for fast execution
- PostgreSQL tests are also available for integration testing
- Fixtures are provided for database session management

## 📦 Dependencies

Core dependencies:
- fastapi - High-performance web framework
- uvicorn - ASGI server for development
- gunicorn - WSGI server for production
- sqlalchemy - SQL toolkit and ORM
- psycopg2-binary - PostgreSQL adapter
- alembic - Database migration tool
- python-dotenv - Environment variable management
- passlib[bcrypt] - Password hashing
- python-jose[cryptography] - JWT implementation
- email-validator - Email validation

Development dependencies:
- pytest - Testing framework
- httpx - HTTP client for testing

## 🏗️ Extending the Template

To add new features to the template:

1. **Add a new model**: Create a new file in `app/models/`
2. **Create schemas**: Define Pydantic schemas in `app/schemas/`
3. **Implement services**: Add business logic in `app/services/`
4. **Create routes**: Define API endpoints in `app/routes/`
5. **Add migrations**: Generate and apply database migrations
6. **Write tests**: Add unit and integration tests in `tests/`

## 📋 Project Documentation

For detailed information about the project architecture and features:
- [Project Summary](PROJECT_SUMMARY.md) - Detailed overview of the project architecture
- [Architecture](ARCHITECTURE.md) - System architecture documentation
- [Authentication Flow](AUTH_FLOW.md) - Detailed authentication implementation
- [Database](DATABASE.md) - Database schema and design
- [Development Guide](DEVELOPMENT_GUIDE.md) - Comprehensive development guide
- [API Documentation](API_DOCUMENTATION.md) - Detailed API endpoint documentation
- [Backup Documentation](BACKUP_DOCUMENTATION.md) - Database backup and restore procedures
- [Docker Troubleshooting Guide](TROUBLESHOOTING_DOCKER.md) - Resolving common Docker container issues

## 🔄 Database Backup

The template includes comprehensive database backup capabilities to ensure data persistence and disaster recovery. You can create backups using the Makefile command:

```bash
make backup
```

This will create a timestamped backup of your PostgreSQL database in the `backups/` directory. For more detailed information about backup strategies, please refer to the [Backup Documentation](BACKUP_DOCUMENTATION.md).

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed information on our code of conduct and development process.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue on the GitHub repository or contact the maintainers.