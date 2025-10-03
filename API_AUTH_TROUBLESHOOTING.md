# API Authentication Troubleshooting Guide

This guide helps diagnose and resolve common authentication issues when working with the FastAPI backend.

## Common 401 "Not Authenticated" Errors

### 1. Token Expiration
**Symptoms**: 
- HTTP 401 error with message `{"detail":"Not authenticated"}`
- Previously working requests suddenly fail

**Cause**: 
JWT tokens expire after 60 minutes by default

**Solution**:
- Obtain a fresh token by re-authenticating
- Implement automatic token refresh in your client

```python
# Example of proper authentication flow
import requests

# 1. Authenticate to get token
auth_response = requests.post(
    "http://localhost:8088/api/auth/login",
    data={
        "username": "manager@example.com",
        "password": "manager123"
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

if auth_response.status_code == 200:
    token_data = auth_response.json()
    access_token = token_data["access_token"]
    
    # 2. Use token for subsequent requests
    headers = {"Authorization": f"Bearer {access_token}"}
    order_response = requests.post(
        "http://localhost:8088/api/orders/",
        json=order_data,
        headers=headers
    )
```

### 2. Invalid Token Format
**Symptoms**: 
- HTTP 401 error with message `{"detail":"Not authenticated"}`
- Token appears to be valid but requests fail

**Cause**: 
Incorrect Authorization header format

**Solution**:
- Ensure the header follows the format: `Authorization: Bearer YOUR_TOKEN_HERE`
- No extra spaces or characters

```python
# Correct format
headers = {"Authorization": f"Bearer {access_token}"}

# Incorrect formats that will fail:
# headers = {"Authorization": access_token}
# headers = {"Authorization": f"Bearer{access_token}"}
# headers = {"Authorization": f"Bearer  {access_token}"}
```

### 3. Database Schema Mismatch
**Symptoms**: 
- HTTP 500 Internal Server Error
- Authentication works but subsequent requests fail

**Cause**: 
Database schema is out of sync with application code

**Solution**:
- Run database migrations to update schema

```bash
# In Docker environment
docker-compose exec web sh -c "cd /app/migrations && alembic upgrade head"
```

## Testing Authentication

### Manual Testing with cURL

```bash
# 1. Authenticate
curl -X POST "http://localhost:8088/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=manager@example.com" \
  -d "password=manager123"

# 2. Use the token from response
curl -X GET "http://localhost:8088/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 3. Submit an order
curl -X POST "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "order": [
      {
        "name": "Burger",
        "price": 8.99,
        "category": "Main Course"
      }
    ],
    "total": 8.99,
    "customer_name": "John Doe",
    "payment_type": "cash"
  }'
```

### Automated Testing

Use the provided test scripts:
- `test_manager_auth.py` - Tests authentication only
- `test_order_submission.py` - Tests order submission with fresh token
- `comprehensive_auth_order_test.py` - Complete authentication and order workflow

## Best Practices

### 1. Token Management
- Always check token expiration before making requests
- Implement automatic re-authentication when tokens expire
- Store tokens securely (avoid localStorage for web apps)

### 2. Error Handling
- Implement retry logic for 401 errors with fresh tokens
- Log authentication failures for debugging
- Provide clear error messages to users

### 3. Database Maintenance
- Run migrations after updating the application
- Regularly backup the database
- Monitor for schema inconsistencies

## Debugging Steps

1. **Verify Services**: Ensure both web and db containers are running
   ```bash
   docker-compose ps
   ```

2. **Test Authentication**: Confirm you can get a valid token
   ```bash
   python test_manager_auth.py
   ```

3. **Check Database**: Ensure the database has the correct schema
   ```bash
   docker-compose exec web sh -c "cd /app/migrations && alembic upgrade head"
   ```

4. **Test with Fresh Token**: Use a newly obtained token for requests
   ```bash
   python comprehensive_auth_order_test.py
   ```

## Common Pitfalls

1. **Using Expired Tokens**: JWT tokens expire after 60 minutes
2. **Incorrect Header Format**: Must be exactly `Bearer TOKEN`
3. **Schema Mismatches**: Database and code must be in sync
4. **Network Issues**: Ensure services are accessible on correct ports

## Contact Support

If issues persist:
1. Check container logs: `docker-compose logs web`
2. Verify database connectivity: `docker-compose exec web python check_users_local.py`
3. Ensure migrations are current: `docker-compose exec web sh -c "cd /app/migrations && alembic current"`