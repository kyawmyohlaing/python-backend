# Frontend Integration Troubleshooting Guide

This guide helps diagnose and resolve common issues when integrating a frontend application (e.g., React at localhost:3000) with the FastAPI backend.

## Common Issue: 401 Authentication Error

### Problem
```
Server error: Failed to submit order: HTTP error! status: 401 - {"detail":"Not authenticated"}
```

### Root Cause
Your frontend is trying to submit an order without proper authentication. The order endpoints require a valid JWT token in the Authorization header.

## Solution

### 1. Understand API Endpoint Requirements

| Endpoint | Authentication Required | Purpose |
|----------|------------------------|---------|
| `GET /api/menu/` | No | Retrieve menu items |
| `GET /api/menu/{id}` | No | Retrieve specific menu item |
| `GET /api/menu/category/{category}` | No | Retrieve menu items by category |
| `POST /api/orders/` | **Yes** | Submit new order |
| `GET /api/orders/` | **Yes** | Retrieve all orders |
| `GET /api/orders/{id}` | **Yes** | Retrieve specific order |

### 2. Proper Authentication Flow

#### Step 1: Authenticate to Get Token
```javascript
// Frontend JavaScript example
async function authenticate() {
  const response = await fetch('http://localhost:8088/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: 'manager@example.com',
      password: 'manager123'
    })
  });
  
  if (response.ok) {
    const data = await response.json();
    // Store token securely (e.g., in state or secure cookie)
    return data.access_token;
  } else {
    throw new Error('Authentication failed');
  }
}
```

#### Step 2: Use Token for Protected Requests
```javascript
// Store the token (example using localStorage - consider more secure options)
let authToken = null;

// Function to get menu (no auth required)
async function getMenu() {
  const response = await fetch('http://localhost:8088/api/menu/');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('Failed to fetch menu');
  }
}

// Function to submit order (auth required)
async function submitOrder(orderData) {
  // Ensure we have a token
  if (!authToken) {
    throw new Error('Not authenticated');
  }
  
  const response = await fetch('http://localhost:8088/api/orders/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authToken}`
    },
    body: JSON.stringify(orderData)
  });
  
  if (response.ok) {
    return await response.json();
  } else {
    const error = await response.json();
    throw new Error(`Failed to submit order: ${error.detail}`);
  }
}

// Complete workflow
async function placeOrder() {
  try {
    // 1. Get menu items
    const menu = await getMenu();
    console.log('Menu:', menu);
    
    // 2. Authenticate
    authToken = await authenticate();
    console.log('Authenticated successfully');
    
    // 3. Submit order
    const orderData = {
      order: [
        {
          name: "Burger",
          price: 8.99,
          category: "Main Course",
          modifiers: ["extra cheese"]
        }
      ],
      total: 8.99,
      customer_name: "John Doe",
      payment_type: "cash"
    };
    
    const order = await submitOrder(orderData);
    console.log('Order submitted:', order);
  } catch (error) {
    console.error('Error:', error.message);
  }
}
```

### 3. Token Management Best Practices

#### Token Refresh
```javascript
class APIClient {
  constructor() {
    this.token = null;
    this.tokenExpiry = null;
  }
  
  async authenticate(username, password) {
    const response = await fetch('http://localhost:8088/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ username, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      this.token = data.access_token;
      // JWT tokens typically expire in 60 minutes (3600 seconds)
      this.tokenExpiry = new Date(Date.now() + 3600000);
      return this.token;
    } else {
      throw new Error('Authentication failed');
    }
  }
  
  isTokenValid() {
    return this.token && this.tokenExpiry && new Date() < this.tokenExpiry;
  }
  
  async getValidToken() {
    if (!this.isTokenValid()) {
      // Re-authenticate with stored credentials
      // (You should securely store credentials for this)
      throw new Error('Token expired and no refresh mechanism implemented');
    }
    return this.token;
  }
  
  async submitOrder(orderData) {
    const token = await this.getValidToken();
    
    const response = await fetch('http://localhost:8088/api/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(orderData)
    });
    
    if (response.ok) {
      return await response.json();
    } else {
      const error = await response.json();
      throw new Error(`Failed to submit order: ${error.detail}`);
    }
  }
}
```

## Common Mistakes to Avoid

### 1. Missing Authorization Header
```javascript
// ❌ Wrong - Missing Authorization header
fetch('http://localhost:8088/api/orders/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
    // Missing Authorization header
  },
  body: JSON.stringify(orderData)
});

// ✅ Correct - Include Authorization header
fetch('http://localhost:8088/api/orders/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + authToken
  },
  body: JSON.stringify(orderData)
});
```

### 2. Incorrect Header Format
```javascript
// ❌ Wrong - Incorrect format
headers: {
  'Authorization': authToken  // Missing "Bearer " prefix
}

// ❌ Wrong - Extra spaces
headers: {
  'Authorization': 'Bearer  ' + authToken  // Extra space
}

// ✅ Correct - Proper format
headers: {
  'Authorization': 'Bearer ' + authToken
}
```

### 3. Using Expired Tokens
```javascript
// ❌ Wrong - Not checking token expiration
const response = await fetch('http://localhost:8088/api/orders/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + possiblyExpiredToken
  },
  // ...
});

// ✅ Correct - Check token validity first
if (!isTokenValid()) {
  await reauthenticate();
}
```

## Debugging Steps

### 1. Verify Backend is Running
```bash
# Check if containers are running
docker-compose ps

# Should show both db and web containers as "Up"
```

### 2. Test Menu Endpoint (No Auth Required)
```bash
# This should work without authentication
curl http://localhost:8088/api/menu/
```

### 3. Test Authentication
```bash
# This should return a token
curl -X POST "http://localhost:8088/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=manager@example.com" \
  -d "password=manager123"
```

### 4. Test Order Submission with Token
```bash
# Replace YOUR_TOKEN_HERE with actual token from step 3
curl -X POST "http://localhost:8088/api/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "order": [
      {
        "name": "Test Item",
        "price": 5.99,
        "category": "Test"
      }
    ],
    "total": 5.99,
    "customer_name": "Test Customer",
    "payment_type": "cash"
  }'
```

## Test Credentials

The database is pre-populated with these test users:

| Role | Username/Email | Password |
|------|----------------|----------|
| Manager | manager@example.com | manager123 |
| Admin | admin@example.com | admin123 |
| Waiter | waiter@example.com | waiter123 |

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (React default)
- `http://localhost:8000` (Alternative)

If you're using a different port, you may need to update the `ALLOWED_ORIGINS` in your environment configuration.

## Additional Resources

1. Run the provided test scripts:
   - `python frontend_integration_example.py` - Complete integration example
   - `python comprehensive_auth_order_test.py` - Advanced authentication handling

2. Check the API documentation:
   - `API_DOCUMENTATION.md` - Complete API reference
   - `AUTH_IMPLEMENTATION_SUMMARY.md` - Authentication details

3. Review the integration guide:
   - `INTEGRATION_GUIDE.md` - Frontend-backend integration specifics