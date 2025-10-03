# Complete Authentication and Order Submission Testing Guide

This comprehensive guide explains how to set up, test, and troubleshoot the authentication flow and order submission in your FastAPI backend.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Server Setup](#server-setup)
4. [Authentication Testing](#authentication-testing)
5. [Order Submission Testing](#order-submission-testing)
6. [Troubleshooting](#troubleshooting)
7. [Curl Command Reference](#curl-command-reference)
8. [Python Script Reference](#python-script-reference)

## Prerequisites

Before testing, ensure you have:

1. **Python 3.8+** installed
2. **PostgreSQL** installed and running on port 5432
3. **Required Python packages** installed:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment variables** configured (see below)

## Database Setup

### 1. Configure Environment Variables

Create a `.env.local` file in the project root with the following content:

```env
# Environment variables for local development
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=BEGmxdg7h0z-TUYdtsJKfXxu-_xVvj3CgFdJy9aK24c
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
DEV_DATABASE_URL=sqlite:///./dev.db
TEST_DATABASE_URL=sqlite:///./test.db
PROD_DATABASE_URL=postgresql://user:password@localhost/prod_db
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
DEFAULT_LEARNING_PATH=beginner
```

### 2. Initialize the Database

Run the database initialization script:

```bash
python init_local_db.py
```

This will create the necessary tables and add the following test users:
- **Admin**: admin@example.com / admin123
- **Manager**: manager@example.com / manager123
- **Waiter**: waiter@example.com / waiter123

## Server Setup

### Starting the FastAPI Server

Start the server in development mode:

```bash
# Option 1: Using uvicorn directly
python -m uvicorn app.main:app --reload --port 8088

# Option 2: Using the start script (if available)
./start.sh

# Option 3: Using make (if available)
make dev
```

The server should be accessible at `http://localhost:8088`

### Verifying Server Status

Check if the server is running:

```bash
curl http://localhost:8088/health
```

Expected response:
```json
{"status": "healthy"}
```

## Authentication Testing

### 1. Login with Test User

Use the admin user to test authentication:

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

### 2. Get Current User Information

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

## Order Submission Testing

### 1. Submit an Order

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

Expected response:
```json
{
  "id": 1,
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
      "category": "Sides",
      "modifiers": []
    }
  ],
  "total": 12.98,
  "table_id": null,
  "customer_count": 1,
  "special_requests": null,
  "timestamp": "2025-10-01T10:00:00",
  "order_type": "dine_in",
  "table_number": null,
  "customer_name": "John Doe",
  "customer_phone": null,
  "delivery_address": null,
  "assigned_seats": null,
  "modifiers": null,
  "payment_type": "cash"
}
```

### 2. Retrieve All Orders

```bash
curl -X GET "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Get Specific Order

```bash
curl -X GET "http://localhost:8088/api/orders/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Connection Refused
**Problem**: `ConnectionError: Failed to establish a new connection`
**Solution**: 
- Ensure the FastAPI server is running on `localhost:8088`
- Check that no firewall is blocking the connection

#### 2. Invalid Credentials
**Problem**: `401 Unauthorized` during login with response `{"detail":"Invalid credentials"}`
**Solution**:
- Verify the username/password (admin@example.com/admin123)
- Check if the database was properly initialized with `init_local_db.py`
- Ensure the database is running and accessible

#### 3. Database Connection Error
**Problem**: `psycopg2.OperationalError: could not translate host name "db" to address`
**Solution**:
- Use the `.env.local` file instead of `.env` for local development
- Ensure PostgreSQL is running on localhost:5432
- Verify database credentials in the `.env.local` file

#### 4. Token Expired
**Problem**: `401 Unauthorized` when accessing protected endpoints
**Solution**: Re-authenticate to get a new token (tokens expire after 60 minutes by default)

#### 5. Invalid JSON
**Problem**: `422 Unprocessable Entity`
**Solution**: Check that your JSON payload matches the expected schema

### Database Troubleshooting

#### Check Database Connection
```bash
# Test PostgreSQL connection
psql -h localhost -p 5432 -U postgres -d mydb
```

#### Reset Database (if needed)
```bash
# Connect to PostgreSQL and drop/recreate database
psql -h localhost -p 5432 -U postgres -c "DROP DATABASE IF EXISTS mydb;"
psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE mydb;"
```

Then reinitialize:
```bash
python init_local_db.py
```

## Curl Command Reference

### Authentication
```bash
# Login
curl -X POST "http://localhost:8088/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com" \
  -d "password=admin123"

# Get current user
curl -X GET "http://localhost:8088/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Orders
```bash
# Submit order
curl -X POST "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"order": [...], "total": 12.98, "customer_name": "John Doe", "payment_type": "cash"}'

# Get all orders
curl -X GET "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get specific order
curl -X GET "http://localhost:8088/api/orders/ORDER_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Users
```bash
# Get all users (admin only)
curl -X GET "http://localhost:8088/api/auth/users" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get specific user
curl -X GET "http://localhost:8088/api/auth/users/USER_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Python Script Reference

### 1. Database Initialization
```bash
python init_local_db.py
```

### 2. Check Users in Database
```bash
python check_users_local.py
```

### 3. Comprehensive Authentication and Order Testing
```bash
python test_auth_and_orders_local.py
```

### 4. Simple Authentication Test
```bash
python test_auth.py
```

## Authentication Flow Summary

1. **Login**: POST to `/api/auth/login` with form data (username, password)
2. **Token**: Receive JWT access token in response
3. **Authorization**: Include token in `Authorization: Bearer YOUR_TOKEN` header
4. **Access**: Use token to access protected endpoints

## Order Submission Flow

1. **Authenticate**: Get valid access token
2. **Prepare**: Create order data matching the OrderCreate schema
3. **Submit**: POST to `/api/orders/` with authorization header
4. **Verify**: Check response for created order details

## Payment Types

The system supports multiple payment types:
- `cash` - Cash payment
- `card` - Credit/debit card payment
- `qr` - QR code payment
- `e_wallet` - Electronic wallet payment
- `gift_card` - Gift card payment

## Role-Based Access Control

Different user roles have different permissions:
- **Admin**: Full access to all endpoints
- **Manager**: Access to analytics and management endpoints
- **Waiter**: Access to order and table management
- **Kitchen**: Access to kitchen order endpoints
- **Cashier**: Access to invoice and payment endpoints

## Example Complete Workflow

1. Start PostgreSQL database
2. Initialize database: `python init_local_db.py`
3. Start the server: `python -m uvicorn app.main:app --reload --port 8088`
4. Test authentication: `python test_auth_and_orders_local.py`
5. Or use curl commands as shown above

This comprehensive testing guide should help you verify that the authentication flow and order submission are working correctly in your FastAPI backend.