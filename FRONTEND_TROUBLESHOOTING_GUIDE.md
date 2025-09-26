# Frontend Troubleshooting Guide for Sales Reports

This guide helps troubleshoot frontend issues with the Sales Reports feature. The backend is confirmed working, so frontend implementation issues are the most likely cause of problems.

## Backend Status Confirmation

The backend API endpoints are working correctly as verified by our tests:
- `GET /api/analytics/reports/daily` ✓ Working
- `GET /api/analytics/reports/weekly` ✓ Working
- `GET /api/analytics/reports/monthly` ✓ Working

## Common Frontend Issues and Solutions

### 1. CORS Issues

**Symptoms**: 
- Network errors in browser console
- Requests blocked by CORS policy
- "No 'Access-Control-Allow-Origin' header" errors

**Solutions**:
- Verify that the backend is configured to allow `http://localhost:3000` in [ALLOWED_ORIGINS](file:///c%3A/strategy_test/python_backend_structure/.env.example#L23-L23)
- Check that the backend is running on the expected port (8088 by default)
- Restart both frontend and backend servers after configuration changes

### 2. Authentication Token Issues

**Symptoms**:
- 401 Unauthorized responses
- "Not enough permissions to access analytics" errors
- "Failed to fetch" errors related to authentication

**Solutions**:
- Ensure the frontend is storing and sending the JWT token correctly
- Verify that the token is being sent in the Authorization header as `Bearer YOUR_TOKEN`
- Check that the user has manager or admin role (sales reports require elevated permissions)

### 3. Incorrect API Endpoint URLs

**Symptoms**:
- 404 Not Found errors
- "Failed to fetch" network errors
- No data loading in the UI

**Solutions**:
- Verify the API endpoints match the backend implementation:
  - Daily: `http://localhost:8088/api/analytics/reports/daily`
  - Weekly: `http://localhost:8088/api/analytics/reports/weekly`
  - Monthly: `http://localhost:8088/api/analytics/reports/monthly`
- Check for typos in URLs
- Ensure the backend server is running on the correct port

### 4. JavaScript/React Implementation Issues

**Symptoms**:
- JavaScript errors in browser console
- Component not rendering
- State management issues

**Solutions**:
- Check browser developer console for JavaScript errors
- Verify API service functions are correctly implemented
- Ensure proper error handling in async functions
- Check React component lifecycle and useEffect dependencies

## Debugging Tools

### 1. Browser Developer Tools

1. Open browser developer tools (F12)
2. Go to the Network tab
3. Reproduce the issue
4. Look for failed requests to the analytics endpoints
5. Check request headers, response status, and response body

### 2. Manual API Testing

Test the backend endpoints directly using curl:

```bash
# First, get an authentication token
curl -X POST "http://localhost:8088/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=manager&password=manager123"

# Use the token to test sales reports
curl -X GET "http://localhost:8088/api/analytics/reports/daily" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Python Debug Script

Use the provided debug script to test API endpoints:

```bash
python debug_frontend_api.py
```

This script will show exactly what the backend is returning, helping to determine if the issue is with the backend or frontend.

## Expected API Response Format

### Daily Sales Report
```json
{
  "period": "daily",
  "start_date": "2025-09-19T15:18:31.541861",
  "end_date": "2025-09-26T15:18:31.541861",
  "total_sales": 8.99,
  "total_orders": 1,
  "average_daily_sales": 8.99,
  "sales_data": [
    {
      "date": "2025-09-25",
      "total_sales": 8.99,
      "order_count": 1,
      "average_order_value": 8.99
    }
  ]
}
```

### Weekly Sales Report
```json
{
  "period": "weekly",
  "start_date": "2025-07-04T15:15:28.216187",
  "end_date": "2025-09-26T15:15:28.216203",
  "total_sales": 8.99,
  "total_orders": 1,
  "average_weekly_sales": 8.99,
  "sales_data": [
    {
      "date": "2025-09-21T00:00:00",
      "total_sales": 8.99,
      "order_count": 1,
      "average_order_value": 8.99
    }
  ]
}
```

### Monthly Sales Report
```json
{
  "period": "monthly",
  "start_date": "2024-09-26T15:15:28.631983",
  "end_date": "2025-09-26T15:15:28.631994",
  "total_sales": 8.99,
  "total_orders": 1,
  "average_monthly_sales": 8.99,
  "sales_data": [
    {
      "date": "2025-09-01T00:00:00",
      "total_sales": 8.99,
      "order_count": 1,
      "average_order_value": 8.99
    }
  ]
}
```

## Frontend Implementation Checklist

### API Service Functions
Ensure your `src/api.js` file has correct implementations:

```javascript
// Example implementation
const API_BASE_URL = 'http://localhost:8088/api';

export const fetchDailySalesReport = async (startDate, endDate) => {
  const token = localStorage.getItem('token'); // or however you store the token
  const params = new URLSearchParams();
  
  if (startDate) params.append('start_date', startDate.toISOString());
  if (endDate) params.append('end_date', endDate.toISOString());
  
  const response = await fetch(
    `${API_BASE_URL}/analytics/reports/daily${params.toString() ? `?${params.toString()}` : ''}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  );
  
  if (!response.ok) {
    throw new Error('Failed to fetch daily sales report');
  }
  
  return response.json();
};

// Similar implementations for weekly and monthly reports
```

### React Component
Ensure your React component properly handles the API responses:

```javascript
// Example component structure
import React, { useState, useEffect } from 'react';

const SalesReportsPage = () => {
  const [activeTab, setActiveTab] = useState('daily');
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchReportData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        let data;
        switch (activeTab) {
          case 'daily':
            data = await fetchDailySalesReport();
            break;
          case 'weekly':
            data = await fetchWeeklySalesReport();
            break;
          case 'monthly':
            data = await fetchMonthlySalesReport();
            break;
          default:
            throw new Error('Invalid tab');
        }
        setReportData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchReportData();
  }, [activeTab]);
  
  // Render UI with loading, error, and data states
};
```

## Additional Debugging Steps

1. **Check Network Tab**: Look for the actual HTTP requests and responses
2. **Verify Token**: Ensure the JWT token is valid and has manager permissions
3. **Check Console**: Look for JavaScript errors that might prevent the component from working
4. **Test with Simple HTML**: Create a simple HTML page with fetch calls to isolate the issue
5. **Compare with Working Endpoints**: Check how other working API calls are implemented in the frontend

## Contact for Further Assistance

If you continue to experience issues after following this guide:
1. Document the exact error messages from browser console
2. Include screenshots of the Network tab showing failed requests
3. Provide details about your frontend implementation
4. Share the output of the debug script: `python debug_frontend_api.py`