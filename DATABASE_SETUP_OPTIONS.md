# Database Setup Options for FastAPI Backend

## Overview

This document explains the two database setup options available for your FastAPI backend:

1. **SQLite** - Simple, file-based database for local development
2. **PostgreSQL in Docker** - Full-featured database for development and production

## Option 1: SQLite (Recommended for Local Development)

SQLite is the easiest option for local development as it requires no separate database server.

### Advantages
- No separate database server needed
- Single file database
- Easy setup and configuration
- Good for development and testing

### Disadvantages
- Not suitable for production
- Limited concurrency
- No advanced PostgreSQL features

### Setup Instructions

1. **Configure Environment Variables**
   Create or update `.env.local` with:
   ```env
   DATABASE_URL=sqlite:///./local.db
   ```

2. **Initialize the Database**
   ```bash
   python init_local_db.py
   ```

3. **Start the Application**
   ```bash
   python -m uvicorn app.main:app --reload --port 8088
   ```

## Option 2: PostgreSQL in Docker (Recommended for Production)

PostgreSQL with Docker provides a full-featured database environment that closely matches production.

### Advantages
- Production-like environment
- Advanced database features
- Better performance and scalability
- Data persistence with volumes

### Disadvantages
- Requires Docker installation
- More complex setup
- Uses system resources

### Setup Instructions

1. **Install Docker**
   - Download from https://www.docker.com/products/docker-desktop
   - Follow installation instructions for your OS

2. **Start the Database Container**
   ```bash
   # Start only the database
   docker-compose up -d db
   
   # Or start all services
   docker-compose up -d
   ```

3. **Verify Container Status**
   ```bash
   docker-compose ps
   ```

4. **Initialize the Database**
   ```bash
   python init_docker_db.py
   ```

5. **Start the Application**
   ```bash
   python -m uvicorn app.main:app --reload --port 8088
   ```

## Connection Configuration

### Environment Variables

The application uses environment variables to configure database connections:

**For SQLite (.env.local):**
```env
DATABASE_URL=sqlite:///./local.db
```

**For Docker PostgreSQL (.env or docker-compose.yml):**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
```

### Connection from Different Contexts

| Context | Host | Port | Database | Username | Password |
|---------|------|------|----------|----------|----------|
| Host Machine | localhost | 5432 | mydb | postgres | password |
| Docker Container | db | 5432 | mydb | postgres | password |

## Database Initialization Scripts

### Local SQLite Initialization
```bash
python init_local_db.py
```

### Docker PostgreSQL Initialization
```bash
python init_docker_db.py
```

Both scripts will:
1. Create database tables
2. Add test users (admin, manager, waiter)
3. Set up proper permissions

## Test Users

All initialization scripts create the same test users:

| Role | Username | Email | Password |
|------|----------|-------|----------|
| Admin | admin | admin@example.com | admin123 |
| Manager | manager | manager@example.com | manager123 |
| Waiter | waiter | waiter@example.com | waiter123 |

## Testing Database Connections

### Check Docker Status
```bash
python check_docker_status.py
```

### Test Database Connection
```bash
# For SQLite
python test_sqlite.py

# For Docker PostgreSQL
python test_docker_db.py
```

## Migration Management

### Alembic Migrations

The project uses Alembic for database migrations:

```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check migration status
alembic current
```

### Manual Table Creation

The initialization scripts automatically create tables, but you can also create them manually:

```bash
# Using the application
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

## Troubleshooting

### Common Issues with SQLite

1. **Permission Errors**
   - Ensure the application has write permissions to the project directory
   - Check file system permissions

2. **Database Locked**
   - Close any applications accessing the database file
   - Restart the application

### Common Issues with Docker PostgreSQL

1. **Port Conflicts**
   - Stop any existing PostgreSQL service on port 5432
   - Change port mapping in docker-compose.yml

2. **Container Not Starting**
   - Check Docker logs: `docker-compose logs db`
   - Ensure Docker has enough resources

3. **Connection Refused**
   - Verify container is running: `docker-compose ps`
   - Check port mapping is correct

### Resetting the Database

#### For SQLite
```bash
# Delete the database file
rm local.db

# Reinitialize
python init_local_db.py
```

#### For Docker PostgreSQL
```bash
# Stop and remove containers with volumes
docker-compose down -v

# Start fresh
docker-compose up -d db

# Reinitialize
python init_docker_db.py
```

## Performance Considerations

### SQLite
- Good for development with single user
- Limited performance with concurrent access
- No connection pooling needed

### PostgreSQL
- Better performance with multiple users
- Connection pooling recommended
- Can be tuned for specific workloads

## Security Considerations

### SQLite
- File-based security
- No network access
- Simple access control

### PostgreSQL
- User-based authentication
- Network security
- SSL support
- Row-level security

## When to Use Each Option

### Use SQLite When:
- Developing locally
- Running tests
- Prototyping
- Learning the system
- Resource-constrained environment

### Use PostgreSQL When:
- Moving to production
- Need advanced database features
- Multiple users accessing simultaneously
- Need data persistence and backup
- Want production-like environment

## Hybrid Approach

You can also use different databases for different environments:

**Development (.env.local):**
```env
DATABASE_URL=sqlite:///./local.db
```

**Production (.env.production):**
```env
DATABASE_URL=postgresql://user:password@prod-host:5432/prod_db
```

## Next Steps

1. **Choose Your Setup**:
   - For quick local development: Use SQLite
   - For production-like environment: Use Docker PostgreSQL

2. **Initialize Database**:
   - SQLite: `python init_local_db.py`
   - Docker: `python init_docker_db.py`

3. **Start Application**:
   ```bash
   python -m uvicorn app.main:app --reload --port 8088
   ```

4. **Test Authentication**:
   ```bash
   python test_auth.py
   ```

Both options are fully supported and will work with all application features.