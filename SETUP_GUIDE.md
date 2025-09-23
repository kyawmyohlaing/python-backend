# Setup Guide

## 🚀 Quick Start

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

## 🧪 Testing the API

Once the application is running, you can test the endpoints:

### 1. Login with the Example User
```bash
curl -X POST http://localhost:8088/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Access Protected Route
Extract the `access_token` from the login response and use it:
```bash
curl http://localhost:8088/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 3. Register a New User
```bash
curl -X POST http://localhost:8088/users/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "securepassword"}'
```

### 4. Login with the New User
```bash
curl -X POST http://localhost:8088/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "securepassword"}'
```

## 🔐 Security Best Practices

### Generating Secure Keys

For production deployments, always generate unique, secure keys for each environment:

1. **Development Environment:**
   ```bash
   python generate_secret.py
   ```
   Copy the output and use it as your `SECRET_KEY` in `.env`

2. **Production Environment:**
   Generate a new key and store it securely (never in version control):
   ```bash
   python generate_secret.py
   ```

3. **Testing Environment:**
   Use a different generated key for testing to ensure isolation.

## 🐳 Docker Setup

### Development Mode (with Hot Reload)
```bash
docker-compose up --build
```

This command:
- Builds the Docker images
- Starts the PostgreSQL database
- Starts the FastAPI application with Uvicorn and hot reload
- Automatically runs Alembic migrations
- Seeds the example user

### Production Mode (with Gunicorn)
```bash
docker-compose -f docker-compose.yml up --build
```

This command:
- Builds the Docker images
- Starts the PostgreSQL database
- Starts the FastAPI application with Gunicorn workers
- Automatically runs Alembic migrations
- Seeds the example user

## 🧪 Testing

### With Docker
```bash
# Run all tests
docker-compose exec web pytest

# Run specific test file
docker-compose exec web pytest tests/test_users.py
```

### Without Docker
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_users.py
```

## 🗃️ Database Migrations

### Running Migrations
```bash
# With Docker
docker-compose exec web alembic upgrade head

# Without Docker
alembic upgrade head
```

### Creating New Migrations
```bash
# With Docker
docker-compose exec web alembic revision --autogenerate -m "Description"

# Without Docker
alembic revision --autogenerate -m "Description"
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use:**
   - Change the port in `docker-compose.yml` or stop the conflicting service

2. **Database connection errors:**
   - Ensure the database service is running
   - Check the `DATABASE_URL` in your `.env` file
   - Run `python test_db_connection.py` for detailed diagnostics

3. **Migration errors:**
   - Run `make migrate` or check migration files
   - Ensure the database is accessible

4. **Permission errors:**
   - Ensure Docker has proper permissions
   - Check file permissions for scripts

### Debugging

1. **Check logs:**
   ```bash
   # Docker logs
   docker-compose logs web
   docker-compose logs db

   # Application logs
   make logs
   ```

2. **Access containers:**
   ```bash
   # Web container
   docker-compose exec web bash

   # Database container
   docker-compose exec db bash
   ```

3. **Test database connection:**
   ```bash
   python test_db_connection.py
   ```

## 📦 Dependencies

### Installing Dependencies
```bash
# With Docker (automatic)
# Dependencies are installed during image build

# Without Docker
pip install -r requirements.txt
```

### Adding New Dependencies
1. Add the package to `requirements.txt`
2. Rebuild the Docker image:
   ```bash
   docker-compose build
   ```
3. Or install directly:
   ```bash
   pip install package-name
   ```

## 🌐 Environment Configuration

### Environment Variables
Create a `.env` file with the following variables:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Different Environments
The application supports different environments:
- **Development**: `ENVIRONMENT=development`
- **Production**: `ENVIRONMENT=production`
- **Testing**: `ENVIRONMENT=testing`

## 🔧 Development Workflow

### Code Structure
```
app/
├── main.py          # Application entry point
├── config.py        # Configuration management
├── database.py      # Database connection setup
├── security.py      # Authentication and password hashing
├── models/          # Database models (SQLAlchemy)
├── schemas/         # Data validation models (Pydantic)
├── routes/          # API endpoints (FastAPI)
├── services/        # Business logic
├── utils/           # Utility functions
└── migrations/      # Database migration scripts
```

### Development Commands
| Command | Description |
|---------|-------------|
| `make dev` | Start development server |
| `make prod` | Start production server |
| `make test` | Run all tests |
| `make migrate` | Run database migrations |
| `make logs` | View application logs |
| `make clean` | Clean temporary files |

### Hot Reload
The development server supports hot reload, which automatically restarts the server when code changes are detected.

## 📚 Documentation

### Project Documentation
- [Project Overview](SUMMARY.md)
- [Architecture](ARCHITECTURE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Authentication Flow](AUTH_FLOW.md)
- [Testing Guide](TESTING_README.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

### API Endpoints
- User management: `/users/`
- Menu management: `/api/menu/`
- Order management: `/api/orders/`
- Kitchen management: `/api/kitchen/`
- Table management: `/api/tables/`
- Invoice management: `/api/invoices/`

## 🤝 Contributing

### Git Workflow
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Code Standards
- Follow PEP 8 style guide
- Write unit tests for new functionality
- Document public APIs
- Use type hints where possible

### Testing
- Write unit tests for business logic
- Write integration tests for API endpoints
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.