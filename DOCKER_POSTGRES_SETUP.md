# Docker PostgreSQL Setup Guide

## Overview

This guide explains how to set up and run PostgreSQL database in Docker for your FastAPI backend application.

## Prerequisites

1. Docker installed on your system
2. Docker Compose installed
3. Basic understanding of Docker commands

## Docker Configuration

The project includes two Docker Compose files:

1. `docker-compose.yml` - Base configuration
2. `docker-compose.override.yml` - Development overrides

### Database Service Configuration

The PostgreSQL database is configured in `docker-compose.yml`:

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
```

## Setting Up PostgreSQL with Docker

### 1. Start the Database Container

```bash
# Start only the database service
docker-compose up -d db

# Or start all services
docker-compose up -d
```

### 2. Verify Container Status

```bash
# Check if containers are running
docker-compose ps

# Or check all Docker containers
docker ps
```

You should see the PostgreSQL container running:

```
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                    NAMES
xxxxxxxxxxxx   postgres:16   "docker-entrypoint.s…"   10 seconds ago   Up 9 seconds    0.0.0.0:5432->5432/tcp   python_backend_structure_db_1
```

### 3. Check Database Logs

```bash
# View database logs
docker-compose logs db
```

Look for messages like:
```
database system is ready to accept connections
```

## Database Connection Details

### From Host Machine (Local Development)

When connecting from your host machine (outside Docker), use:

- **Host**: localhost
- **Port**: 5432
- **Database**: mydb
- **Username**: postgres
- **Password**: password

Connection string: `postgresql://postgres:password@localhost:5432/mydb`

### From Docker Container (Application)

When connecting from another Docker container in the same network, use:

- **Host**: db (service name in docker-compose)
- **Port**: 5432
- **Database**: mydb
- **Username**: postgres
- **Password**: password

Connection string: `postgresql://postgres:password@db:5432/mydb`

## Initializing the Database

### 1. Run Database Migrations

The application automatically runs migrations on startup, but you can also run them manually:

```bash
# Run migrations
docker-compose exec web alembic upgrade head
```

### 2. Initialize Sample Data

The application includes initialization scripts that create sample data:

- Sample menu items
- Default admin user

These are created automatically when the application starts for the first time.

## Testing Database Connection

### 1. Using Docker Exec

```bash
# Connect to the database container
docker-compose exec db psql -U postgres -d mydb

# Run SQL commands
\dt  -- List tables
SELECT * FROM users LIMIT 5;  -- View sample users
\q  -- Quit
```

### 2. Using Python Script

Run the test script to verify connection:

```bash
python test_docker_db.py
```

### 3. Using psql (if installed locally)

```bash
# Connect from host machine
psql -h localhost -p 5432 -U postgres -d mydb
```

## Common Issues and Solutions

### 1. Port Already in Use

**Problem**: `Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address already in use`

**Solution**: 
- Stop any existing PostgreSQL service on your host machine
- Or change the port mapping in docker-compose.yml:
  ```yaml
  ports:
    - "5433:5432"  # Map host port 5433 to container port 5432
  ```

### 2. Connection Refused

**Problem**: `could not connect to server: Connection refused`

**Solution**:
- Ensure the Docker container is running: `docker-compose ps`
- Check container logs: `docker-compose logs db`
- Verify port mapping is correct

### 3. Authentication Failed

**Problem**: `FATAL: password authentication failed for user "postgres"`

**Solution**:
- Verify credentials match docker-compose.yml
- Reset the database volume if needed:
  ```bash
  docker-compose down -v
  docker-compose up -d db
  ```

### 4. Database Not Initialized

**Problem**: Tables don't exist

**Solution**:
- Ensure the application has run its initialization code
- Run migrations manually: `docker-compose exec web alembic upgrade head`

## Data Persistence

The database data is persisted using Docker volumes:

```yaml
volumes:
  postgres_data:
```

This ensures data is not lost when containers are stopped or removed.

To reset the database completely:

```bash
# Stop containers and remove volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Environment Variables

The database configuration can be customized using environment variables in your `.env` file:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb
POSTGRES_PORT=5432
```

## Backup and Restore

### Create Backup

```bash
# Create a database dump
docker-compose exec db pg_dump -U postgres mydb > backup.sql
```

### Restore Backup

```bash
# Restore from a database dump
docker-compose exec -T db psql -U postgres mydb < backup.sql
```

## Performance Considerations

For production use, consider these optimizations:

1. **Resource Limits**:
   ```yaml
   db:
     # ... other config
     deploy:
       resources:
         limits:
           memory: 1G
           cpus: '0.5'
   ```

2. **Custom PostgreSQL Configuration**:
   ```yaml
   db:
     # ... other config
     command: postgres -c shared_buffers=256MB -c max_connections=50
   ```

## Security Considerations

1. **Change Default Password**: Update `POSTGRES_PASSWORD` in production
2. **Remove Trust Authentication**: Replace `POSTGRES_HOST_AUTH_METHOD: trust` with proper authentication
3. **Use Secrets**: For sensitive data in production environments
4. **Network Isolation**: Use custom networks for better isolation

## Next Steps

1. Start the database: `docker-compose up -d db`
2. Initialize the application: `docker-compose up -d`
3. Test the connection: `python test_docker_db.py`
4. Access the API at `http://localhost:8088`

The database is now ready for use with your FastAPI backend application!