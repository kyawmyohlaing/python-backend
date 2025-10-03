# Orders Status Tracker Implementation Guide

## Overview
This guide provides instructions for implementing the Orders Status Tracker page in the React frontend. The issue "Failed to load orders" is likely due to missing authentication or incorrect API endpoint usage.

## Files to Create

### 1. OrdersStatusTracker.jsx
Create this file in `c:\strategy_test\react_frontend\src\OrdersStatusTracker.jsx`:

```jsx
import React, { useState, useEffect } from 'react';
import { fetchOrders } from './api';

const OrdersStatusTracker = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch orders using the API service
      const ordersData = await fetchOrders();
      setOrders(ordersData);
    } catch (err) {
      console.error('Failed to load orders:', err);
      setError(err.message || 'Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="orders-status-tracker">
        <h1>Orders Status Tracker</h1>
        <div>Loading orders...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="orders-status-tracker">
        <h1>Orders Status Tracker</h1>
        <div className="error-message">
          Error: {error}
          <button onClick={loadOrders}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="orders-status-tracker">
      <h1>Orders Status Tracker</h1>
      
      {orders.length === 0 ? (
        <div>No orders found</div>
      ) : (
        <div className="orders-list">
          <table>
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Table</th>
                <th>Total</th>
                <th>Type</th>
                <th>Timestamp</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.customer_name || 'N/A'}</td>
                  <td>{order.table_number || 'N/A'}</td>
                  <td>${order.total?.toFixed(2) || '0.00'}</td>
                  <td>{order.order_type || 'N/A'}</td>
                  <td>{order.timestamp ? new Date(order.timestamp).toLocaleString() : 'N/A'}</td>
                  <td>
                    <span className={`status-badge status-${order.status || 'pending'}`}>
                      {order.status || 'pending'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      <div className="refresh-section">
        <button onClick={loadOrders}>Refresh Orders</button>
      </div>
    </div>
  );
};

export default OrdersStatusTracker;
```

### 2. OrdersStatusTracker.css
Create this file in `c:\strategy_test\react_frontend\src\OrdersStatusTracker.css`:

```css
.orders-status-tracker {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.orders-status-tracker h1 {
  color: #333;
  margin-bottom: 20px;
}

.error-message {
  color: #d32f2f;
  background-color: #ffebee;
  padding: 15px;
  border-radius: 4px;
  margin: 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-message button {
  background-color: #d32f2f;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.error-message button:hover {
  background-color: #b71c1c;
}

.orders-list {
  overflow-x: auto;
}

.orders-list table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.orders-list th,
.orders-list td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.orders-list th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.orders-list tr:hover {
  background-color: #f9f9f9;
}

.orders-list tr:last-child td {
  border-bottom: none;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.status-pending {
  background-color: #fff3e0;
  color: #f57c00;
}

.status-preparing {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status-ready {
  background-color: #e8f5e9;
  color: #388e3c;
}

.status-served {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.status-delivered {
  background-color: #ede7f6;
  color: #651fff;
}

.refresh-section {
  margin-top: 20px;
  text-align: center;
}

.refresh-section button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.refresh-section button:hover {
  background-color: #1565c0;
}
```

## Required API Service Updates

Ensure the `fetchOrders` function in `c:\strategy_test\react_frontend\src\api.js` is correctly implemented:

```javascript
export const fetchOrders = async () => {
  // Define the fetch function for retry purposes
  const fetchOrdersFunc = async (retryCount = 0) => {
    const response = await fetch(`${API_BASE_URL}/orders`, {
      headers: getAuthHeaders()
    });
    return handleFetchError(response, fetchOrdersFunc, retryCount);
  };

  try {
    const response = await fetchOrdersFunc();
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch orders:', error);
    throw new Error('Failed to fetch orders. Please make sure the backend is running.');
  }
};
```

## Common Issues and Solutions

### 1. Authentication Issues
If orders still don't load, check:
- The user is logged in
- The authentication token is stored in localStorage
- The token is being sent with the request
- The token hasn't expired

### 2. Network Issues
- Verify the backend is running on `http://localhost:8088`
- Check that the API endpoint `/api/orders` is accessible
- Ensure CORS is properly configured

### 3. Data Format Issues
- Check the actual response format from the API
- Ensure the frontend code matches the response structure
- Handle null or missing values appropriately

## Testing the Implementation

### 1. Manual Testing
1. Navigate to the Orders Status Tracker page
2. Verify that orders load correctly
3. Check that authentication is working
4. Test error scenarios (offline, server down)

### 2. Browser Developer Tools
1. Open Network tab
2. Refresh the page
3. Check that the request to `/api/orders`:
   - Has the correct Authorization header
   - Returns a 200 status code
   - Returns the expected JSON data

### 3. Console Logs
Check the browser console for any JavaScript errors that might prevent the page from loading.

## Expected Behavior After Implementation

1. ✅ Orders Status Tracker page loads without errors
2. ✅ Orders are displayed in a table format
3. ✅ Each order shows ID, customer, table, total, type, timestamp, and status
4. ✅ Status badges are color-coded
5. ✅ Refresh button works correctly
6. ✅ Error messages are displayed appropriately

## Troubleshooting

### If Orders Still Don't Load
1. Check browser Network tab for request details
2. Verify the authentication token is being sent
3. Check browser console for JavaScript errors
4. Verify backend is running on the correct port

### If Authentication Fails
1. Ensure user is logged in
2. Check that the token is stored in localStorage
3. Verify token expiration handling
4. Test login functionality

### If Data Format Issues Occur
1. Check the actual API response format
2. Adjust frontend code to match the response structure
3. Handle missing or null values appropriately