# Sales Reports Feature Testing Guide

This guide provides instructions for testing the Daily/Weekly/Monthly Sales Reports feature that has been implemented in both the FastAPI backend and React frontend.

## Overview

The sales reports feature includes:
1. Backend API endpoints for retrieving daily, weekly, and monthly sales data
2. Frontend React component for displaying the reports
3. API service functions for communicating between frontend and backend

## Backend Testing

### 1. Test API Endpoints Directly

You can test the backend endpoints using curl or a tool like Postman:

```bash
# Test daily sales report
curl -X GET "http://localhost:8000/api/analytics/reports/daily" -H "Authorization: Bearer YOUR_TOKEN"

# Test weekly sales report
curl -X GET "http://localhost:8000/api/analytics/reports/weekly" -H "Authorization: Bearer YOUR_TOKEN"

# Test monthly sales report
curl -X GET "http://localhost:8000/api/analytics/reports/monthly" -H "Authorization: Bearer YOUR_TOKEN"

# Test with date filters
curl -X GET "http://localhost:8000/api/analytics/reports/daily?start_date=2025-01-01&end_date=2025-01-31" -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. Run the Python Test Script

```bash
cd c:\strategy_test\python_backend_structure
python test_sales_reports.py
python test_analytics_service.py
```

## Frontend Testing

### 1. Test API Service Functions

The API service functions in `src/api.js` should be tested to ensure they:
- Correctly construct URLs for the sales report endpoints
- Handle date filters properly
- Return data in the expected format

### 2. Test the SalesReportsPage Component

The SalesReportsPage.jsx component should be tested to ensure it:
- Renders correctly
- Fetches data from the API service functions
- Displays daily, weekly, and monthly reports in tabs
- Handles loading and error states
- Allows date filtering

### 3. Manual UI Testing

1. Start the React frontend:
   ```bash
   cd c:\strategy_test\react_frontend
   npm run dev
   ```

2. Navigate to the Sales Reports page (typically at `/sales-reports`)

3. Verify that:
   - The page loads without errors
   - All three tabs (Daily, Weekly, Monthly) are visible
   - Data loads correctly when switching between tabs
   - Date filters work as expected
   - Data is displayed in a readable format

## Integration Testing

### 1. End-to-End Flow

1. Start both the FastAPI backend and React frontend
2. Log in as a manager user (sales reports require manager access)
3. Navigate to the Sales Reports page
4. Verify that data loads correctly for each report type
5. Test date filtering functionality
6. Check that the UI updates correctly when data changes

### 2. Data Consistency

Verify that the data shown in daily, weekly, and monthly reports is consistent:
- The sum of daily reports for a week should match the weekly report
- The sum of daily reports for a month should match the monthly report

## Test Data Preparation

If you need to prepare test data:

1. Ensure there are orders in the database with various dates
2. Make sure there are different order types (dine-in, takeaway, delivery)
3. Include orders with discounts and taxes to verify calculations

## Common Issues to Watch For

1. **Authentication Issues**: Sales reports require manager-level access
2. **Date Formatting**: Ensure dates are properly formatted in API requests
3. **Empty Data Handling**: Verify the UI handles cases with no data gracefully
4. **Performance**: Large date ranges might impact performance
5. **Timezone Issues**: Ensure date calculations account for timezones correctly

## Automated Testing

Run the provided test scripts:

```bash
# Backend tests
python test_sales_reports.py
python test_analytics_service.py

# Frontend tests (if you have a testing framework set up)
npm test test_frontend_sales_reports.js
```

## Troubleshooting

### If the frontend fails to load:
1. Check that the Vite development server is running
2. Verify that the api.js file has correct syntax (no template literal errors)
3. Ensure the backend is accessible

### If the backend endpoints return errors:
1. Check that the analytics service methods are implemented
2. Verify database connectivity
3. Confirm that authentication is working properly
4. Check the logs for specific error messages

### If data doesn't display correctly:
1. Verify that the API service functions return data in the expected format
2. Check that the React component properly handles the data
3. Look for JavaScript console errors in the browser

## Expected Results

When fully functional, the sales reports feature should:
1. Display accurate sales data for daily, weekly, and monthly periods
2. Allow filtering by date range
3. Show summary statistics (total orders, revenue, discounts, taxes, net revenue)
4. Have a responsive UI that works on different screen sizes
5. Properly handle error cases and empty data scenarios
6. Restrict access to manager users only

## Additional Verification

1. Check that the feature is properly documented in README.md
2. Verify that all new endpoints are documented in API_DOCUMENTATION.md
3. Confirm that the database schema supports the required analytics queries
4. Ensure that the feature follows the project's coding standards and patterns