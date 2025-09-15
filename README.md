# FastAPI Backend Skeleton with Postgres, JWT & Alembic

A complete FastAPI backend template featuring PostgreSQL database integration, JWT authentication, Alembic migrations, and a well-structured architecture. This template provides a solid foundation for building scalable web applications with proper separation of concerns.

## Features

- ✅ **FastAPI**: Modern, fast (high-performance) web framework for building APIs
- ✅ **PostgreSQL**: Robust relational database with SQLAlchemy ORM
- ✅ **JWT Authentication**: Secure token-based authentication system
- ✅ **Alembic Migrations**: Database schema version control
- ✅ **Docker Support**: Containerized development and deployment
- ✅ **Structured Architecture**: Clean separation of models, schemas, routes, and services
- ✅ **Comprehensive Testing**: Pytest suite for API endpoints
- ✅ **CORS Support**: Cross-origin resource sharing configuration
- ✅ **Environment Configuration**: Flexible configuration management
- ✅ **Menu Management**: Complete CRUD operations for menu items with categories

## Project Structure

```
app/
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas for validation
├── routes/          # API route definitions
├── services/        # Business logic implementations
├── utils/           # Utility functions
├── database.py      # Database configuration
├── config.py        # Configuration management
├── security.py      # Authentication and security utilities
├── dependencies.py  # Dependency injection
├── main.py          # FastAPI application entry point
```

## Menu Management

The template includes a complete menu management system with the following features:

- **Create Menu Items**: Add new menu items with name, price, and category
- **Batch Creation**: Add multiple menu items in a single request
- **Read Menu Items**: Retrieve all menu items or specific items by ID
- **Update Menu Items**: Modify existing menu items
- **Delete Menu Items**: Remove menu items from the database
- **Category Management**: Filter menu items by category or get all unique categories
- **Duplicate Prevention**: Automatic prevention of duplicate menu item names
- **Error Handling**: Comprehensive error handling for all operations

### Menu API Endpoints

- `GET /api/menu` - Get all menu items
- `POST /api/menu` - Create a new menu item
- `POST /api/menu/batch` - Create multiple menu items
- `GET /api/menu/{id}` - Get a specific menu item
- `PUT /api/menu/{id}` - Update a menu item
- `DELETE /api/menu/{id}` - Delete a menu item
- `GET /api/menu/category/{category}` - Get menu items by category
- `GET /api/menu/categories` - Get all unique menu categories

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env` file
4. Run database migrations: `alembic upgrade head`
5. Start the server: `uvicorn app.main:app --reload`

## Docker Deployment

The template includes Docker support for easy deployment:

```bash
docker-compose up -d
```

## Testing

Run the test suite with pytest:

```bash
pytest
```

## Documentation

- [API Documentation](DOCUMENTATION.md)
- [Development Guide](DEVELOPMENT_GUIDE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
