# FastAPI Backend Template

A production-ready FastAPI backend template with PostgreSQL, Alembic, JWT authentication, and Docker support. This template provides a solid foundation for building scalable, secure web APIs with Python and FastAPI.

## 🌟 Features

- **FastAPI** - Modern, fast (high-performance) web framework for building APIs
- **PostgreSQL** - Production-ready database with persistent storage
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool with automatic seeding
- **JWT Authentication** - Secure token-based authentication
- **Bcrypt** - Password hashing for security
- **Pydantic** - Data validation and settings management
- **Docker** - Containerization for easy deployment
- **Gunicorn** - Production-ready WSGI server
- **Hot Reload** - Development mode with automatic reloading

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-github-repo-url>
cd fastapi-backend-template

# Copy the environment file
cp .env.example .env

# Start in development mode (with hot reload)
make dev

# Or start in production mode (with Gunicorn workers)
make prod
```

The application will be available at `http://localhost:8000`.

## 📁 Project Structure

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

## 🛠️ Makefile Commands

```bash
make dev       # Start development (hot reload)
make prod      # Start production (Gunicorn)
make down      # Stop all containers
make logs      # View web logs
make migrate   # Run Alembic migrations
make test      # Run tests
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
# Login with the example user
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Access protected route (replace <access_token> with the token from the login response)
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

## 🐳 Docker Setup

The template includes a complete Docker setup with separate configurations for development and production:

- **Development**: Uses Uvicorn with hot reload
- **Production**: Uses Gunicorn with multiple workers
- **PostgreSQL**: Persistent database storage
- **Automatic Migrations**: Alembic migrations run on startup

## 🧪 Testing

The template includes comprehensive tests:

```bash
# Run unit tests
make test

# Or run directly
python -m pytest tests/
```

## 📦 Dependencies

- fastapi
- uvicorn
- gunicorn
- sqlalchemy
- psycopg2-binary
- alembic
- python-dotenv
- passlib[bcrypt]
- python-jose[cryptography]

## 📋 Project Summary

For a detailed overview of the project architecture and features, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.