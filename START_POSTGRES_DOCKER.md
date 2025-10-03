# Starting PostgreSQL Database in Docker

## Quick Start Guide

This guide explains how to start the PostgreSQL database in Docker for your FastAPI backend.

## Prerequisites

1. Docker installed on your system
2. Docker Compose installed
3. This project repository cloned

## Starting the Database

### 1. Start Only the Database Container

```bash
# Navigate to the project directory
cd c:\strategy_test\python_backend_structure

# Start only the PostgreSQL database container
docker-compose up -d db
```

### 2. Verify the Container is Running

```bash
# Check container status
docker-compose ps

# You should see output like:
# Name                          Command              State           Ports
# ----------------------------------------------------------------------------------
# python_backend_structure_db_1   docker-entrypoint.sh postgres   Up      0.0.0.0:5432->5432/tcp
```

### 3. Check Database Logs

```bash
# View database logs to ensure it's ready
docker-compose logs db

# Look for messages like:
# database system is ready to accept connections
```

## Testing the Database Connection

### 1. Run the Test Script

```bash
python test_docker_db.py
```

Expected output:
```
Attempting to connect to Docker PostgreSQL database...
Using connection string: postgresql://postgres:password@localhost:5432/mydb
✅ Successfully connected to Docker PostgreSQL database!
PostgreSQL version: PostgreSQL 16.x ...
Existing tables: []
```

### 2. Manual Connection Test

```bash
# If you have psql installed locally
psql -h localhost -p 5432 -U postgres -d mydb

# Default password is 'password'
```

## Initializing the Database

### 1. Run the Initialization Script

```bash
python init_docker_db.py
```

This will:
- Create database tables
- Add test users (admin, manager, waiter)
- Set up proper permissions

### 2. Verify Initialization

```bash
python test_docker_db.py
```

Expected output after initialization:
```
Attempting to connect to Docker PostgreSQL database...
Using connection string: postgresql://postgres:password@localhost:5432/mydb
✅ Successfully connected to Docker PostgreSQL database!
PostgreSQL version: PostgreSQL 16.x ...
Existing tables: ['users', 'orders', 'menu_items', ...]
```

## Common Commands

### Managing Containers

```bash
# Start all services
docker-compose up -d

# Stop database container
docker-compose stop db

# Start database container
docker-compose start db

# Restart database container
docker-compose restart db

# View logs
docker-compose logs db

# Stop and remove containers
docker-compose down

# Stop and remove containers with volumes (destroys data)
docker-compose down -v
```

### Database Management

```bash
# Connect to database shell
docker-compose exec db psql -U postgres -d mydb

# Run migrations (if needed)
docker-compose exec web alembic upgrade head
```

## Troubleshooting

### 1. Container Won't Start

```bash
# Check detailed logs
docker-compose logs db

# Ensure no other service is using port 5432
netstat -an | findstr 5432
```

### 2. Connection Refused

```bash
# Verify container is running
docker-compose ps

# Check if port is mapped correctly
docker port python_backend_structure_db_1
```

### 3. Authentication Failed

```bash
# Verify credentials in docker-compose.yml
# Default: postgres / password

# Reset database if needed
docker-compose down -v
docker-compose up -d db
```

### 4. Data Persistence Issues

```bash
# Check if volume is properly configured
docker volume ls | grep postgres

# Data is stored in the 'postgres_data' volume
```

## Environment Details

### Database Configuration

- **Host**: localhost (from host machine) or db (from Docker container)
- **Port**: 5432
- **Database**: mydb
- **Username**: postgres
- **Password**: password

### Connection Strings

**From Host Machine:**
```
postgresql://postgres:password@localhost:5432/mydb
```

**From Docker Container:**
```
postgresql://postgres:password@db:5432/mydb
```

## Next Steps

1. **Start the database**: `docker-compose up -d db`
2. **Initialize the database**: `python init_docker_db.py`
3. **Test the connection**: `python test_docker_db.py`
4. **Start the application**: `python -m uvicorn app.main:app --reload --port 8088`
5. **Test authentication**: `python test_auth.py`

The PostgreSQL database is now ready for use with your FastAPI backend application!