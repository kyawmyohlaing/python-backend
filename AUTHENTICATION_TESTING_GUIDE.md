# Authentication and Order Submission Testing Guide

This guide provides instructions for testing the authentication flow and order submission using both curl commands and a Python script.

## Prerequisites

1. Ensure the FastAPI server is running on `localhost:8088`
2. Make sure the database has been initialized with sample data
3. Install required dependencies: `pip install requests`

## Default Test User

The system creates a default admin user during initialization:
- **Username/Email**: `admin@example.com`
- **Password**: `admin123`

## Testing with Curl Commands

### 1. Authentication (Login)

```bash
# Login using form data
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

Replace `YOUR_ACCESS_TOKEN` with the token from the login response:

```bash
curl -X GET "http://localhost:8088/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Submit an Order

Replace `YOUR_ACCESS_TOKEN` with your actual token:

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

### 4. Retrieve All Orders

```bash
curl -X GET "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Specific Order

Replace `ORDER_ID` with an actual order ID:

```bash
curl -X GET "http://localhost:8088/api/orders/ORDER_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing with Python Script

Run the comprehensive test script:

```bash
python test_auth_and_orders.py
```

This script will:
1. Test unauthorized access (should be rejected)
2. Authenticate with the API
3. Retrieve current user information
4. Submit a sample order
5. Retrieve all orders

## Common Issues and Solutions

### 1. Connection Refused
**Problem**: `ConnectionError: Failed to establish a new connection`
**Solution**: Make sure the FastAPI server is running on `localhost:8088`

### 2. Invalid Credentials
**Problem**: `401 Unauthorized` during login
**Solution**: 
- Verify the username/password (admin@example.com/admin123)
- Check if the database was properly initialized

### 3. Token Expired
**Problem**: `401 Unauthorized` when accessing protected endpoints
**Solution**: Re-authenticate to get a new token

### 4. Invalid JSON
**Problem**: `422 Unprocessable Entity`
**Solution**: Check that your JSON payload matches the expected schema

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

Different user roles may have different permissions:
- **Admin**: Full access to all endpoints
- **Manager**: Access to analytics and management endpoints
- **Waiter**: Access to order and table management
- **Kitchen**: Access to kitchen order endpoints
- **Cashier**: Access to invoice and payment endpoints

## Troubleshooting Tips

1. **Check Server Logs**: Look at the FastAPI server console for error messages
2. **Verify Database**: Ensure PostgreSQL is running and accessible
3. **Check Environment Variables**: Verify `.env` file configuration
4. **Network Issues**: Ensure no firewall is blocking the connection
5. **Token Scope**: Make sure your user role has permission for the requested operation

## Example Complete Workflow

1. Start the server: `make dev` or `python -m uvicorn app.main:app --reload`
2. Run the test script: `python test_auth_and_orders.py`
3. Or use curl commands as shown above

This testing guide should help you verify that the authentication flow and order submission are working correctly in your FastAPI backend.