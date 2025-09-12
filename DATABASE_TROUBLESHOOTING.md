# Database Troubleshooting Guide

This document provides a comprehensive guide for troubleshooting database issues in the FastAPI backend template, particularly focusing on PostgreSQL configuration and common problems encountered during setup.

## Table of Contents
1. [Overview](#overview)
2. [PostgreSQL Configuration](#postgresql-configuration)
3. [Common Issues and Solutions](#common-issues-and-solutions)
4. [Database Initialization](#database-initialization)
5. [Verification Steps](#verification-steps)
6. [Docker-specific Issues](#docker-specific-issues)

## Overview

The FastAPI backend template is designed to work with PostgreSQL as the primary database. However, it can be configured to work with other databases as well. This guide focuses on troubleshooting PostgreSQL-related issues.

## PostgreSQL Configuration

### Environment Variables

The database configuration is primarily controlled through environment variables in the `.env` file:

```env
# Database settings
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
DEV_DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb_test
PROD_DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb_prod
```

### Docker Configuration

When running in Docker, the database URL needs to reference the service name instead of localhost:

```yaml
# In docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
```

The application connects to the database using `postgresql://postgres:password@db:5432/mydb` where `db` is the service name.

### Configuration Files

The database configuration is handled in the following files:

1. `app/config.py` - Contains the configuration classes
2. `app/database.py` - Handles database connection setup
3. `app/migrations/env.py` - Alembic migration environment configuration

## Common Issues and Solutions

### 1. Connection Refused Errors

**Problem**: 
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
```

**Solution**:
- Ensure PostgreSQL is running
- Check if you're running in Docker and using the correct service name (`db` instead of `localhost`)
- Verify the database credentials in the `.env` file
- Check if the PostgreSQL port is correctly exposed in Docker

### 2. Authentication Failed Errors

**Problem**: 
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: password authentication failed for user "postgres"
```

**Solution**:
- Verify the PostgreSQL username and password in the `.env` file
- Check the PostgreSQL container logs to ensure it started correctly
- Ensure the PostgreSQL user has the correct permissions

### 3. Module Import Errors

**Problem**: 
```
ModuleNotFoundError: No module named 'app'
```

**Solution**:
- Ensure the Python path is correctly set when running scripts
- When running scripts inside Docker containers, make sure the working directory is set correctly
- Check that the application files are correctly copied to the container

### 4. Database Tables Not Created

**Problem**: 
- API endpoints return empty results
- Database queries return no data

**Solution**:
- Run Alembic migrations to create the database tables
- Verify that the database initialization script has been run
- Check the database connection to ensure tables exist

## Database Initialization

### Automatic Initialization

The database is automatically initialized when the application starts through the `start.sh` script:

1. Wait for PostgreSQL to be ready
2. Run Alembic migrations
3. Initialize the database with sample data

### Manual Initialization

To manually initialize the database:

1. Ensure the database services are running:
   ```bash
   docker-compose up -d db
   ```

2. Run the initialization script:
   ```bash
   docker-compose exec web python /app/init_postgres.py
   ```

### Sample Data

The initialization script populates the database with sample data including:
- Menu items (Burger, Pizza, Salad, Soda, Coffee, Tea Leaf Salad, Chicken Curry, Steak (Grill), Wine, Beer)
- Users (admin user with username "admin" and password "admin123")

## Verification Steps

### 1. Check Database Services

```bash
# Check if services are running
docker-compose ps

# Expected output should show both db and web services as "Up"
```

### 2. Verify Database Connection

```bash
# Connect to the database and list tables
docker-compose exec db psql -U postgres -d mydb -c "\dt"

# Expected output should show all application tables:
# - alembic_version
# - kitchen_orders
# - menu_items
# - orders
# - tables
# - users
```

### 3. Check Table Data

```bash
# Check menu items
docker-compose exec db psql -U postgres -d mydb -c "SELECT name, price, category FROM menu_items;"

# Expected output should show all sample menu items
```

### 4. Test API Endpoints

```bash
# Test the menu API endpoint
curl http://localhost:8088/api/menu/

# Expected output should show JSON data with menu items
```

## Docker-specific Issues

### 1. Container Restarting

**Problem**: 
- Web container keeps restarting

**Solution**:
- Check the container logs for specific error messages:
  ```bash
  docker logs <container_name>
  ```
- Ensure the database service is running before starting the web service
- Verify that all configuration files are correctly set up

### 2. Network Issues

**Problem**: 
- Application cannot connect to the database

**Solution**:
- Ensure both services are on the same Docker network
- Verify the service name is used instead of localhost
- Check the Docker Compose configuration for network settings

### 3. Volume Issues

**Problem**: 
- Database data is lost when containers are removed

**Solution**:
- Use Docker volumes to persist database data:
  ```yaml
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ```

## Best Practices

1. **Environment Configuration**:
   - Always use environment variables for database configuration
   - Keep sensitive information like passwords in environment variables
   - Use different database URLs for development, testing, and production

2. **Docker Configuration**:
   - Use service names instead of localhost when connecting from one container to another
   - Ensure proper volume configuration for data persistence
   - Use health checks to ensure services are ready before starting dependent services

3. **Database Initialization**:
   - Always run migrations when deploying new versions
   - Use initialization scripts to populate the database with sample data
   - Backup production data before making schema changes

4. **Error Handling**:
   - Implement proper error handling for database operations
   - Log database errors for debugging purposes
   - Provide meaningful error messages to API clients

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)