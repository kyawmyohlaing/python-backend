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
- Analytics and sales reporting system (daily, weekly, monthly reports)

## Prerequisites

- Python 3.11
- Docker and Docker Compose
- Make (for command automation)

## Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your environment variables
3. Run `make dev` for development or `make prod` for production

## Database Setup

The application uses PostgreSQL as its primary database. By default, it's configured to work with the Docker setup provided, but you can also configure it to work with an external PostgreSQL database.

### Default Docker Setup

The default configuration uses:
- Username: `postgres`
- Password: `password`
- Database: `mydb`
- Host: `db` (Docker service name)
- Port: `5432`

### Custom Database Configuration

If you need to use different credentials or an external database:

1. Update the `DATABASE_URL` in your `.env` file:
   ```env
   DATABASE_URL=postgresql://your_username:your_password@your_host:5432/your_database
   ```

2. If using Docker with custom credentials, also update `docker-compose.yml`:
   ```yaml
   services:
     db:
       environment:
         POSTGRES_USER: your_username
         POSTGRES_PASSWORD: your_password
         POSTGRES_DB: your_database
   ```

3. Test your database connection:
   ```bash
   python test_db_connection.py
   ```

### Troubleshooting Database Issues

If you encounter database connection issues:

1. Run the connection test script:
   ```bash
   python test_db_connection.py
   ```

2. Check the detailed troubleshooting guides:
   - [Database Troubleshooting](DATABASE_TROUBLESHOOTING.md)
   - [General Troubleshooting](TROUBLESHOOTING.md)

3. If you've changed credentials, reset the database volume:
   ```bash
   docker-compose down -v
   make dev
   ```

## API Endpoints

- `/api/users/` - User management
- `/api/menu/` - Menu management
- `/api/orders/` - Order management
- `/api/kitchen/` - Kitchen display system
- `/api/tables/` - Table management
- `/api/invoices/` - Invoice management
- `/api/analytics/` - Analytics and sales reporting

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

### Testing Sales Reports Feature

Special tests are available for the sales reports feature:

```bash
python test_sales_reports.py
python test_analytics_service.py
```

See [SALES_REPORTS_TESTING_GUIDE.md](SALES_REPORTS_TESTING_GUIDE.md) for detailed testing instructions.

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