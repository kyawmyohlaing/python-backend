# Frontend Menu.Page Authentication Troubleshooting Guide

## Problem
```
Server error: Failed to submit order: HTTP error! status: 401 - {"detail":"Not authenticated"}
```

This error occurs when the menu.page frontend tries to submit an order without proper authentication. The order submission endpoint (`POST /api/orders/`) requires a valid JWT token in the Authorization header.

## Root Cause Analysis

Based on the project structure and previous work, the issue is likely in the frontend's authentication implementation. The frontend needs to:

1. Properly authenticate with the backend to obtain a JWT token
2. Store the token securely
3. Include the token in the Authorization header when submitting orders
4. Handle token expiration and refresh

## Solution

### 1. Verify Frontend API Service Implementation

The frontend should have an API service file (typically `src/api.js`) that handles authentication and order submission. Here's what this implementation should look like:

```javascript
// src/api.js

// Base URL configuration
const API_BASE_URL = '/api'; // Using proxy

// Helper to get authentication headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// Login function
export const login = async (username, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Login failed: ${errorText}`);
    }

    const data = await response.json();
    
    // Store token with expiration
    const expiry = new Date();
    expiry.setMinutes(expiry.getMinutes() + 59); // Token expires in 60 minutes
    
    localStorage.setItem('authToken', data.access_token);
    localStorage.setItem('tokenExpiry', expiry.toISOString());
    
    return data;
  } catch (error) {
    console.error('Login failed:', error);
    throw new Error(`Login failed: ${error.message}`);
  }
};

// Check if token is still valid
export const isTokenValid = () => {
  const token = localStorage.getItem('authToken');
  const expiry = localStorage.getItem('tokenExpiry');
  
  if (!token || !expiry) return false;
  
  return new Date() < new Date(expiry);
};

// Ensure authentication before making requests
export const ensureAuth = async () => {
  if (!isTokenValid()) {
    // Use default credentials for menu.page
    // In a production app, you might want to prompt the user
    await login('manager@example.com', 'manager123');
  }
};

// Submit order function
export const submitOrder = async (orderData) => {
  console.log('📤 Submitting order:', orderData);
  
  try {
    // Ensure we have valid authentication
    await ensureAuth();
    
    const response = await fetch(`${API_BASE_URL}/orders/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(orderData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Failed to submit order: ${errorData.detail || response.statusText}`);
    }

    const createdOrder = await response.json();
    console.log('✅ Order submitted successfully:', createdOrder);
    
    return createdOrder;
  } catch (error) {
    console.error('Failed to submit order:', error);
    throw new Error(`Failed to submit order: ${error.message}`);
  }
};
```

### 2. Verify Vite Configuration

The frontend should have a `vite.config.js` file with proper proxy configuration:

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8088',
        changeOrigin: true,
        secure: false,
      }
    }
  }
});
```

### 3. Menu.Page Component Implementation

The menu.page component should properly use the API service:

```javascript
// src/MenuPage.jsx or similar
import React, { useState } from 'react';
import { submitOrder } from './api'; // Adjust path as needed

const MenuPage = () => {
  const [cart, setCart] = useState([]);
  const [customerInfo, setCustomerInfo] = useState({
    name: '',
    phone: '',
    paymentType: 'cash'
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleCheckout = async () => {
    try {
      setSubmitting(true);
      setError(null);
      
      // Prepare order data
      const orderData = {
        order: cart.map(item => ({
          name: item.name,
          price: item.price,
          category: item.category || 'food',
          modifiers: item.modifiers || []
        })),
        total: cart.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0),
        customer_name: customerInfo.name || 'Customer',
        customer_phone: customerInfo.phone || '',
        payment_type: customerInfo.paymentType || 'cash'
      };
      
      // Submit order
      const order = await submitOrder(orderData);
      
      // Handle successful order submission
      console.log('Order submitted successfully:', order);
      // Clear cart, show success message, etc.
      
    } catch (error) {
      console.error('Checkout failed:', error);
      setError(error.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      {/* Menu page content */}
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <button 
        onClick={handleCheckout} 
        disabled={submitting || cart.length === 0}
      >
        {submitting ? 'Processing...' : 'Checkout'}
      </button>
    </div>
  );
};

export default MenuPage;
```

## Debugging Steps

### 1. Check Browser Developer Tools

Open your browser's developer tools (F12) and:

1. Go to the Network tab
2. Try to checkout from menu.page
3. Look for the failed request to `/api/orders/`
4. Check the request headers - is there an Authorization header?
5. Check the response - what does the 401 error say exactly?

### 2. Verify Token Storage

In the browser console, check if the token is being stored:

```javascript
// Check if token exists
console.log('Auth token:', localStorage.getItem('authToken'));
console.log('Token expiry:', localStorage.getItem('tokenExpiry'));

// Check if token is valid
const expiry = localStorage.getItem('tokenExpiry');
if (expiry) {
  console.log('Token expired:', new Date() > new Date(expiry));
}
```

### 3. Test Authentication Flow

Create a simple test to verify the authentication works:

```javascript
// In browser console or a test component
import { login, isTokenValid } from './src/api'; // Adjust path

// Test login
login('manager@example.com', 'manager123')
  .then(data => {
    console.log('Login successful:', data);
    console.log('Token valid:', isTokenValid());
  })
  .catch(error => {
    console.error('Login failed:', error);
  });
```

### 4. Test Order Submission

Test order submission with a simple function:

```javascript
// In browser console or a test component
import { submitOrder } from './src/api'; // Adjust path

const testOrder = {
  order: [
    {
      name: "Test Item",
      price: 5.99,
      category: "Test",
      modifiers: []
    }
  ],
  total: 5.99,
  customer_name: "Test Customer",
  payment_type: "cash"
};

submitOrder(testOrder)
  .then(order => console.log('Order submitted:', order))
  .catch(error => console.error('Order failed:', error));
```

## Common Issues and Fixes

### Issue 1: Token Not Being Stored
**Symptom**: `localStorage.getItem('authToken')` returns null
**Fix**: Check the login function implementation and ensure it's correctly storing the token

### Issue 2: Token Expired
**Symptom**: Token exists but is expired
**Fix**: Implement token refresh or re-authentication logic

### Issue 3: Authorization Header Missing
**Symptom**: Network tab shows request to `/api/orders/` without Authorization header
**Fix**: Ensure the `getAuthHeaders()` function is being used correctly

### Issue 4: Proxy Configuration Issues
**Symptom**: Requests going to wrong URL or CORS errors
**Fix**: Verify `vite.config.js` proxy configuration

## Test Credentials

The database contains these test users:

| Role | Username/Email | Password |
|------|----------------|----------|
| Manager | manager@example.com | manager123 |
| Admin | admin@example.com | admin123 |
| Waiter | waiter@example.com | waiter123 |

## Additional Recommendations

1. **Add Better Error Handling**: Improve error messages to help diagnose issues
2. **Implement Token Refresh**: Add logic to automatically refresh tokens before they expire
3. **Add Loading States**: Show loading indicators during authentication and order submission
4. **Validate Input**: Ensure customer information is properly validated before submission

## Conclusion

The 401 error occurs because the frontend is not properly handling authentication for order submission. By implementing the proper authentication flow as described above and following the debugging steps, you should be able to resolve this issue.

The key points to remember:
1. Authenticate before submitting orders
2. Store and use the JWT token correctly
3. Include the token in the Authorization header
4. Handle token expiration appropriately