# Menu.Page Checkout Troubleshooting Guide

## Problem
```
Server error: Failed to submit order: HTTP error! status: 401 - {"detail":"Not authenticated"}
```

## Root Cause
The error occurs when your menu.page frontend tries to submit an order without proper authentication. The order submission endpoint (`POST /api/orders/`) requires a valid JWT token in the Authorization header.

## Solution

### 1. Understand the Authentication Flow

The correct flow for checkout should be:

1. **User visits menu.page**
2. **User adds items to cart**
3. **User proceeds to checkout**
4. **Frontend authenticates with backend** (if not already authenticated)
5. **Frontend submits order with authentication token**

### 2. Proper Implementation for menu.page

#### Step 1: Check Authentication Status
```javascript
// Check if user is already authenticated
let authToken = localStorage.getItem('authToken');
let tokenExpiry = localStorage.getItem('tokenExpiry');

function isTokenValid() {
  if (!authToken || !tokenExpiry) return false;
  return new Date() < new Date(tokenExpiry);
}
```

#### Step 2: Authenticate if Needed
```javascript
async function authenticate() {
  // If we already have a valid token, use it
  if (isTokenValid()) {
    return authToken;
  }
  
  // Otherwise, authenticate with backend
  const response = await fetch('http://localhost:8088/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: 'manager@example.com',  // Or use actual user credentials
      password: 'manager123'
    })
  });
  
  if (response.ok) {
    const data = await response.json();
    authToken = data.access_token;
    
    // Store token and expiry (tokens expire in 60 minutes)
    localStorage.setItem('authToken', authToken);
    const expiry = new Date();
    expiry.setMinutes(expiry.getMinutes() + 59); // Set expiry to 59 minutes
    localStorage.setItem('tokenExpiry', expiry.toISOString());
    
    return authToken;
  } else {
    throw new Error('Authentication failed');
  }
}
```

#### Step 3: Submit Order with Authentication
```javascript
async function submitOrder(orderData) {
  try {
    // Ensure we have a valid token
    const token = await authenticate();
    
    // Submit order with authentication
    const response = await fetch('http://localhost:8088/api/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(orderData)
    });
    
    if (response.ok) {
      const order = await response.json();
      return order;
    } else {
      const error = await response.json();
      throw new Error(`Order submission failed: ${error.detail}`);
    }
  } catch (error) {
    console.error('Error submitting order:', error);
    throw error;
  }
}
```

#### Step 4: Complete Checkout Flow
```javascript
async function checkout(cartItems, customerInfo) {
  try {
    // Prepare order data
    const orderData = {
      order: cartItems.map(item => ({
        name: item.name,
        price: item.price,
        category: item.category,
        modifiers: item.modifiers || []
      })),
      total: cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0),
      customer_name: customerInfo.name,
      customer_phone: customerInfo.phone || '',
      payment_type: customerInfo.paymentType || 'cash',
      // Add other fields as needed
    };
    
    // Submit order
    const order = await submitOrder(orderData);
    
    console.log('Order submitted successfully:', order);
    return order;
  } catch (error) {
    console.error('Checkout failed:', error);
    throw new Error(`Checkout failed: ${error.message}`);
  }
}
```

### 3. Common Mistakes to Avoid

#### ❌ Missing Authorization Header
```javascript
// Wrong - No authentication
fetch('http://localhost:8088/api/orders/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(orderData)
});
```

#### ✅ Correct - With Authentication
```javascript
// Correct - With authentication
fetch('http://localhost:8088/api/orders/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authToken}`
  },
  body: JSON.stringify(orderData)
});
```

#### ❌ Using Expired Tokens
```javascript
// Wrong - Not checking token expiration
const response = await fetch('http://localhost:8088/api/orders/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
  },
  // ...
});
```

#### ✅ Correct - Checking Token Validity
```javascript
// Correct - Check token validity first
if (!isTokenValid()) {
  await authenticate(); // Get new token
}
```

### 4. Debugging Steps

#### Step 1: Verify Backend is Running
```bash
# Check Docker containers
docker-compose ps

# Should show both db and web containers as "Up"
```

#### Step 2: Test Authentication Endpoint
```bash
# Test login endpoint
curl -X POST "http://localhost:8088/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=manager@example.com" \
  -d "password=manager123"
```

#### Step 3: Test Order Submission with Token
```bash
# Replace YOUR_TOKEN_HERE with actual token from step 2
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

### 5. Test Credentials

The database contains these test users:

| Role | Username/Email | Password |
|------|----------------|----------|
| Manager | manager@example.com | manager123 |
| Admin | admin@example.com | admin123 |
| Waiter | waiter@example.com | waiter123 |

### 6. CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (React default)
- `http://localhost:8000` (Alternative)

If menu.page uses a different origin, you may need to update the `ALLOWED_ORIGINS` in your environment configuration.

### 7. Example Working Implementation

Here's a complete example of how to implement checkout in menu.page:

```javascript
class MenuPageCheckout {
  constructor() {
    this.baseURL = 'http://localhost:8088';
    this.authToken = null;
  }
  
  async authenticate() {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/login`, {
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
        this.authToken = data.access_token;
        return this.authToken;
      } else {
        throw new Error('Authentication failed');
      }
    } catch (error) {
      console.error('Authentication error:', error);
      throw error;
    }
  }
  
  async submitOrder(orderData) {
    if (!this.authToken) {
      await this.authenticate();
    }
    
    try {
      const response = await fetch(`${this.baseURL}/api/orders/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.authToken}`
        },
        body: JSON.stringify(orderData)
      });
      
      if (response.ok) {
        return await response.json();
      } else {
        const error = await response.json();
        throw new Error(`Order submission failed: ${error.detail}`);
      }
    } catch (error) {
      console.error('Order submission error:', error);
      throw error;
    }
  }
  
  async checkout(cartItems, customerInfo) {
    const orderData = {
      order: cartItems.map(item => ({
        name: item.name,
        price: item.price,
        category: item.category || 'food',
        modifiers: item.modifiers || []
      })),
      total: cartItems.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0),
      customer_name: customerInfo.name || 'Customer',
      payment_type: customerInfo.paymentType || 'cash'
    };
    
    return await this.submitOrder(orderData);
  }
}

// Usage example:
// const checkout = new MenuPageCheckout();
// try {
//   const order = await checkout.checkout(cartItems, customerInfo);
//   console.log('Order placed:', order);
// } catch (error) {
//   console.error('Checkout failed:', error);
// }
```

## Conclusion

The 401 error occurs because menu.page is trying to submit an order without proper authentication. Implement the authentication flow described above, ensuring that:

1. You authenticate with the backend before submitting orders
2. You include the JWT token in the Authorization header
3. You handle token expiration and refresh appropriately
4. You test the integration thoroughly

This should resolve the authentication error and allow successful order submission from menu.page.