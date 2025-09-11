# FastAPI Backend Template - Comprehensive Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [API Endpoints](#api-endpoints)
6. [Database Design](#database-design)
7. [Authentication & Security](#authentication--security)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Development Workflow](#development-workflow)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)

## Project Overview
This is a production-ready, scalable FastAPI backend template designed for building secure, high-performance web APIs with Python. It provides a standardized foundation for API development with built-in user management, database integration, authentication, and containerized deployment.

## System Architecture
The backend follows a layered architecture pattern with clear separation of concerns:
- **Presentation Layer**: FastAPI routes and request/response handling
- **Business Logic Layer**: Services and dependency injection
- **Data Access Layer**: SQLAlchemy models and database sessions
- **External Integration Layer**: PostgreSQL database, Docker containers

## Technology Stack
- **Framework**: FastAPI 0.68.0+
- **ASGI Server**: Uvicorn 0.15.0+ (development), Gunicorn 20.1.0+ (production)
- **Database**: PostgreSQL with SQLAlchemy 1.4.0+ ORM
- **Database Migrations**: Alembic 1.7.0+
- **Authentication**: JWT with Python-JOSE, Password hashing with Passlib/Bcrypt
- **Configuration**: python-dotenv 0.19.0+
- **Data Validation**: Pydantic 1.8.0+
- **Testing**: pytest 6.2.4+, httpx 0.18.0+
- **Containerization**: Docker and Docker Compose

## Project Structure
```
app/
├── main.py                 # Application entry point
├── config.py               # Configuration management
├── database.py             # Database connection setup
├── security.py             # Security utilities (JWT, hashing)
├── dependencies.py         # Dependency injection
├── models/                 # Database models (SQLAlchemy)
├── schemas/                # Data validation models (Pydantic)
├── routes/                 # API endpoints (FastAPI)
├── services/               # Business logic
├── utils/                  # Utility functions
├── data/                   # Shared data modules
├── migrations/             # Database migration scripts
tests/                      # Unit and integration tests
docs/                       # Documentation files
docker-compose.yml          # Production services
docker-compose.override.yml # Development overrides
Dockerfile                  # Container definition
Makefile                    # Workflow automation
requirements.txt            # Python dependencies
```

## API Endpoints

### User Management
- `POST /users/register` - Register a new user
- `POST /users/login` - Login and get JWT token
- `GET /users/me` - Get current user info
- `GET /users/` - List all users (admin only)

### Menu Management
- `GET /api/menu` - Get all menu items

### Order Management
- `GET /api/orders` - Get all orders
- `GET /api/orders/{order_id}` - Get specific order
- `POST /api/orders` - Create new order
- `PUT /api/orders/{order_id}` - Update order
- `DELETE /api/orders/{order_id}` - Delete order

### Kitchen Management
- `GET /api/kitchen/orders` - Get all kitchen orders
- `PUT /api/kitchen/orders/{order_id}` - Update kitchen order status
- `DELETE /api/kitchen/orders/{order_id}` - Remove order from kitchen

### Table & Seat Management
- `GET /api/tables` - Get all tables
- `GET /api/tables/{table_id}` - Get specific table
- `POST /api/tables` - Create new table
- `PUT /api/tables/{table_id}` - Update table
- `DELETE /api/tables/{table_id}` - Delete table
- `POST /api/tables/{table_id}/assign/{order_id}` - Assign table to order
- `POST /api/tables/{table_id}/release` - Release table
- `POST /api/tables/{table_id}/assign-seat/{seat_number}` - Assign specific seat
- `POST /api/tables/{table_id}/release-seat/{seat_number}` - Release specific seat
- `POST /api/tables/merge-tables/{table_id_1}/{table_id_2}` - Merge two tables
- `POST /api/tables/split-bill/{table_id}` - Split bill at table
- `GET /api/tables/occupied/` - Get all occupied tables
- `GET /api/tables/available/` - Get all available tables

## Database Design

### Users Table
- `id` (Integer, Primary Key)
- `name` (String)
- `email` (String, Unique)
- `hashed_password` (String)
- `created_at` (DateTime)

### Menu Items Table
- `id` (Integer, Primary Key)
- `name` (String)
- `price` (Float)
- `category` (String)

### Orders Table
- `id` (Integer, Primary Key)
- `total` (Float)
- `timestamp` (DateTime)
- `order_data` (Text, JSON string of order items)
- `table_id` (Integer, Foreign Key to tables)
- `customer_count` (Integer)
- `special_requests` (String)
- `assigned_seats` (String, JSON string of assigned seats)

### Kitchen Orders Table
- `id` (Integer, Primary Key)
- `order_id` (Integer, Foreign Key to orders)
- `status` (String: pending, preparing, ready)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Tables Table
- `id` (Integer, Primary Key)
- `table_number` (Integer, Unique)
- `capacity` (Integer)
- `is_occupied` (Boolean)
- `current_order_id` (Integer, Foreign Key to orders)
- `status` (String: available, occupied, reserved, cleaning)
- `seats` (JSON, array of seat objects)

## Authentication & Security

### JWT Authentication
- Token-based authentication using HS256 algorithm
- Access tokens with configurable expiration
- Secure token refresh mechanism
- Protected routes with dependency injection

### Password Security
- bcrypt hashing for password storage
- Secure password validation
- Protection against timing attacks

### Security Best Practices
- Environment-based configuration
- CORS middleware configuration
- SQL injection protection through SQLAlchemy ORM
- Input validation with Pydantic schemas

## Testing

### Test Structure
```
tests/
├── conftest.py              # pytest fixtures
├── test_example.py          # Basic test example
├── test_users.py            # User model tests
├── test_users_api.py        # User API endpoint tests
├── test_users_postgres.py   # PostgreSQL user tests
├── test_table_management.py # Table & Seat Management tests
```

### Running Tests
```bash
# Run all tests
make test

# Run table management tests specifically
make test-tables

# Run tests with pytest directly
pytest tests/test_table_management.py -v
```

### Test Categories for Table Management
1. **Table CRUD Operations** - Create, read, update, delete tables
2. **Table Assignment** - Assign tables to orders and release them
3. **Seat Management** - Assign and release individual seats
4. **Merge/Split Functionality** - Merge tables and split bills
5. **Table Status Queries** - Get available and occupied tables
6. **Error Handling** - Proper error responses for invalid operations

### Test Data Management
- Automatic cleanup using pytest fixtures
- Isolated test environments
- No residual test data
- Realistic test data generation

## Deployment

### Containerized Deployment
- Docker multi-stage build process
- Production-ready Gunicorn with Uvicorn workers
- Environment-based configuration
- Health check endpoints

### Environment Configuration
- `.env` file for environment variables
- Docker Compose for service orchestration
- Separate configurations for development and production

### Scaling Considerations
- Gunicorn worker configuration
- Database connection pooling
- Load balancing capabilities
- Monitoring and logging integration

## Development Workflow

### Getting Started
1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run `make dev` for development environment
4. Access API at `http://localhost:8000`

### Development Commands
```bash
make dev          # Start development server
make prod         # Start production server
make test         # Run all tests
make test-tables  # Run table management tests
make migrate      # Run database migrations
make logs         # View container logs
make clean        # Clean Python cache files
```

### Database Migrations
```bash
# Generate new migration
alembic revision --autogenerate -m "Migration description"

# Apply migrations
alembic upgrade head
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify PostgreSQL is running
- Check `.env` database configuration
- Ensure Docker networking is correct

#### Migration Problems
- Check migration file syntax
- Verify database connectivity
- Review migration history with `alembic history`

#### Authentication Errors
- Validate JWT secret key configuration
- Check token expiration settings
- Verify password hashing implementation

### Debugging Tools
- Container logs with `make logs`
- Interactive debugging with `docker-compose exec`
- Database inspection with `psql`
- API testing with Postman or curl

## Contributing

### Code Standards
- Follow PEP 8 Python style guide
- Use type hints for all function signatures
- Write comprehensive docstrings
- Include unit tests for new functionality

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request with description

### Testing Requirements
- Maintain or improve test coverage
- Pass all existing tests
- Include tests for new features
- Document test scenarios
