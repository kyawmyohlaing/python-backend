# FastAPI Backend Template

A production-ready FastAPI backend template with PostgreSQL, JWT authentication, Alembic migrations, and Docker support.

## 🚀 Features

- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Production-ready database with connection pooling
- **JWT Authentication**: Secure token-based authentication
- **Alembic**: Database migration management
- **Docker**: Containerized deployment with separate dev/prod configs
- **Gunicorn/Uvicorn**: Production server with hot reload for development
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: ORM for database operations
- **Environment-based Configuration**: Flexible configuration management
- **Comprehensive Testing**: Unit and integration tests included
- **CORS Support**: Cross-origin resource sharing configuration
- **Makefile**: Simplified development commands
- **Documentation**: Extensive documentation and examples

## 🏁 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-backend-template
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env to set your SECRET_KEY
   ```

3. **Start the development server**
   ```bash
   make dev
   ```

   Or with Docker:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   The application will be available at `http://localhost:8088`.

## 📚 Documentation

- [Project Overview](SUMMARY.md)
- [Setup Guide](SETUP_GUIDE.md)
- [Development Guide](DEVELOPMENT_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Authentication Flow](AUTH_FLOW.md)
- [Testing Guide](TESTING_README.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## 🧪 Testing

Run the test suite:
```bash
make test
```

Or with Docker:
```bash
docker-compose exec web pytest
```

## 🐳 Docker Setup

The template includes a complete Docker setup with separate configurations for development and production:

- **Development**: Uses Uvicorn with hot reload
- **Production**: Uses Gunicorn with multiple workers
- **PostgreSQL**: Persistent database storage
- **Automatic Migrations**: Alembic migrations run on startup

## 🧪 Testing

- Unit tests for business logic
- Integration tests for API endpoints
- Support for both SQLite and PostgreSQL
- Test runner script included

## 📦 Dependencies

- fastapi
- uvicorn
- gunicorn
- sqlalchemy
- psycopg2-binary
- alembic
- python-dotenv

## 🛠️ Development Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start development server |
| `make prod` | Start production server |
| `make test` | Run all tests |
| `make migrate` | Run database migrations |
| `make logs` | View application logs |
| `make clean` | Clean temporary files |

## 🔐 Authentication Flow

1. Register a new user account (password is hashed)
2. Login with email/password to receive JWT token
3. Use JWT token in Authorization header for protected routes
4. Retrieve user profile information

## 🧪 API Testing

Test the API endpoints with cURL:

```bash
# Login with the example user
curl -X POST http://localhost:8088/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Access protected route (replace YOUR_TOKEN_HERE with actual token)
curl http://localhost:8088/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🗃️ Database Migrations

Generate and apply migrations:
```bash
# Generate a new migration
docker-compose exec web alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec web alembic upgrade head
```

## 📖 Project Structure

```
.
├── app/                 # Main application code
│   ├── main.py          # Application entry point
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection setup
│   ├── security.py      # Authentication and password hashing
│   ├── models/          # Database models (SQLAlchemy)
│   ├── schemas/         # Data validation models (Pydantic)
│   ├── routes/          # API endpoints (FastAPI)
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   └── migrations/      # Database migration scripts
├── tests/               # Unit and integration tests
├── Dockerfile           # Production Docker configuration
├── docker-compose.yml   # Production services configuration
├── docker-compose.override.yml  # Development environment overrides
├── Makefile             # Development commands
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.