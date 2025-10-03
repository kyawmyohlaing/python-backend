# Authentication Setup and Testing Guide

## Overview

This guide explains how to set up and test the authentication system in your FastAPI backend. The system uses JWT tokens for authentication and supports role-based access control.

## Prerequisites

1. Python 3.8+
2. Required Python packages installed (`pip install -r requirements.txt`)
3. A working database (SQLite for local development, PostgreSQL for production)

## Database Setup Options

### Option 1: SQLite (Recommended for Local Development)

SQLite is the easiest option for local development as it requires no separate database server.

1. **Configure Environment Variables**
   Create or update `.env.local` with:
   ```env
   DATABASE_URL=sqlite:///./local.db
   ```

2. **Initialize the Database**
   ```bash
   python init_local_db.py
   ```

### Option 2: PostgreSQL (For Production)

If you want to use PostgreSQL:

1. **Install PostgreSQL**
   - Download from https://www.postgresql.org/download/
   - Follow installation instructions for your OS

2. **Start PostgreSQL Service**
   - On Windows: Start the PostgreSQL service
   - On macOS: `brew services start postgresql`
   - On Linux: `sudo systemctl start postgresql`

3. **Create Database and User**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database and user
   CREATE DATABASE mydb;
   CREATE USER postgres WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE mydb TO postgres;
   \q
   ```

4. **Configure Environment Variables**
   Update `.env.local` with:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
   ```

5. **Initialize the Database**
   ```bash
   python init_local_db.py
   ```

## Starting the Server

Start the FastAPI server:

```bash
# Option 1: Direct uvicorn command
python -m uvicorn app.main:app --reload --port 8088

# Option 2: Using the start script (if available)
./start.sh

# Option 3: Using make (if available)
make dev
```

The server will be available at `http://localhost:8088`

## Testing Authentication

### 1. Test Server Health

```bash
curl http://localhost:8088/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Login with Test User

Use one of the test users created during database initialization:

```bash
curl -X POST "http://localhost:8088/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com" \
  -d "password=admin123"
```

Expected response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Current User Information

Use the access token from the login response:

```bash
curl -X GET "http://localhost:8088/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected response:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": null,
  "role": "admin",
  "created_at": "2025-10-01T10:00:00",
  "updated_at": "2025-10-01T10:00:00"
}
```

### 4. Submit an Order

Use the access token to submit an order:

```bash
curl -X POST "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order": [
      {
        "name": "Burger",
        "price": 8.99,
        "category": "Main Course",
        "modifiers": ["extra cheese"]
      },
      {
        "name": "Fries",
        "price": 3.99,
        "category": "Sides"
      }
    ],
    "total": 12.98,
    "customer_name": "John Doe",
    "payment_type": "cash"
  }'
```

### 5. Retrieve All Orders

```bash
curl -X GET "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Test Users

The initialization script creates the following test users:

| Role | Username | Email | Password |
|------|----------|-------|----------|
| Admin | admin | admin@example.com | admin123 |
| Manager | manager | manager@example.com | manager123 |
| Waiter | waiter | waiter@example.com | waiter123 |

## Role-Based Access Control

Different endpoints require different roles:

- **Admin**: Full access to all endpoints
- **Manager**: Access to analytics and management endpoints
- **Waiter**: Access to order and table management
- **Kitchen**: Access to kitchen order endpoints
- **Cashier**: Access to invoice and payment endpoints

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure the FastAPI server is running
   - Check that the port is correct (default: 8088)

2. **Invalid Credentials**
   - Verify username/password
   - Check if the database was initialized properly

3. **Database Connection Errors**
   - Verify database credentials in `.env.local`
   - Ensure the database service is running
   - Check firewall settings

4. **Token Expired**
   - Re-authenticate to get a new token
   - Default token expiration: 60 minutes

### Checking Database Content

To verify database content:

```bash
python check_users_local.py
```

## Python Test Scripts

### Comprehensive Authentication Test

```bash
python test_auth_and_orders_local.py
```

### Simple Authentication Test

```bash
python test_auth.py
```

### Database Initialization

```bash
python init_local_db.py
```

## API Endpoints

### Authentication Endpoints

- **POST** `/api/auth/login` - User login
- **GET** `/api/auth/me` - Get current user
- **POST** `/api/auth/register` - Register new user

### Protected Endpoints

- **POST** `/api/orders/` - Create order
- **GET** `/api/orders/` - Get all orders
- **GET** `/api/orders/{id}` - Get specific order
- **PUT** `/api/orders/{id}` - Update order
- **DELETE** `/api/orders/{id}` - Delete order

All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Security Features

- **JWT Tokens**: Secure, signed tokens with expiration
- **Password Hashing**: Bcrypt hashing for secure password storage
- **Role-Based Access**: Different permissions for different user roles
- **Protected Routes**: Automatic validation of authentication tokens

## Conclusion

The authentication system is ready for use. You can:

1. Start with SQLite for easy local development
2. Test authentication with the provided test users
3. Use the API endpoints to submit orders and manage data
4. Extend the system with additional roles or features as needed

The system follows best practices for security and is suitable for production use with proper configuration.