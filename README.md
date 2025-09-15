# FastAPI Backend Skeleton

A production-ready, scalable FastAPI backend template designed for building secure, high-performance web APIs with Python.

## Features

- FastAPI-based RESTful API framework
- PostgreSQL integration with SQLAlchemy ORM
- JWT-based authentication and user management
- Alembic for database migrations
- Dockerized development and production environments
- Comprehensive test suite with pytest
- Database backup and restore capabilities
- Order management system
- Menu management system
- Kitchen display system (KDS) integration
- Table management system
- Invoice generation and management system

## Prerequisites

- Python 3.11
- Docker and Docker Compose
- Make (for command automation)

## Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your environment variables
3. Run `make dev` for development or `make prod` for production

## API Endpoints

- `/api/users/` - User management
- `/api/menu/` - Menu management
- `/api/orders/` - Order management
- `/api/kitchen/` - Kitchen display system
- `/api/tables/` - Table management
- `/api/invoices/` - Invoice management

## Development

### Running the Application

For development:
```bash
make dev
```

For production:
```bash
make prod
```

### Running Tests

```bash
make test
```

### Database Migrations

```bash
make migrate
```

## Project Structure

```
app/
├── models/          # Database models (SQLAlchemy)
├── schemas/         # Data validation models (Pydantic)
├── routes/          # API endpoints (FastAPI)
├── services/        # Business logic
├── utils/           # Utility functions
├── migrations/      # Database migration scripts
├── config.py        # Configuration management
├── database.py      # Database connection setup
├── security.py      # Security utilities (JWT, hashing)
└── main.py          # Application entry point

tests/               # Unit and integration tests
```

## Documentation

- [API Documentation](API_DOCUMENTATION.md) - Complete API endpoint documentation
- [Architecture](ARCHITECTURE.md) - System architecture overview
- [Authentication Flow](AUTH_FLOW.md) - JWT authentication implementation
- [Database Management](DATABASE.md) - Database setup and management
- [Invoice API](INVOICE_API.md) - Invoice generation and management
- [Kitchen API](KITCHEN_API.md) - Kitchen display system integration
- [KOT Documentation](KOT.md) - Kitchen Order Ticket printing
- [Order Entry API](ORDER_ENTRY_API.md) - Order management system
- [Table Management API](TABLE_MANAGEMENT_API.md) - Table assignment and management
- [Development Guide](DEVELOPMENT_GUIDE.md) - Developer setup and workflow

## License

This project is licensed under the terms described in the [LICENSE](LICENSE) file.