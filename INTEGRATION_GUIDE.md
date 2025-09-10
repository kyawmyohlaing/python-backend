# React Frontend Integration Guide

This document explains how to integrate the React frontend with the Python FastAPI backend.

## API Endpoints

The backend now provides the following API endpoints that match the frontend expectations:

### Menu Endpoints

1. **Get Menu Items**
   - URL: `/api/menu`
   - Method: `GET`
   - Description: Retrieve all available menu items
   - Response: Array of menu items

2. **Create Menu Item**
   - URL: `/api/menu`
   - Method: `POST`
   - Description: Create a new menu item
   - Request Body: Menu item data
   - Response: Created menu item with ID

### Order Endpoints

1. **Submit Order**
   - URL: `/api/orders`
   - Method: `POST`
   - Description: Submit a new order
   - Request Body: Order data
   - Response: Created order with ID and timestamp

2. **Get Orders**
   - URL: `/api/orders`
   - Method: `GET`
   - Description: Retrieve all submitted orders
   - Response: Array of all orders

## Data Models

### Menu Item
```json
{
  "id": 1,
  "name": "Shan Noodles",
  "price": 2.5,
  "category": "Myanmar Food"
}
```

### Order
```json
{
  "id": 1,
  "order": [
    {
      "name": "Shan Noodles",
      "price": 2.5,
      "category": "Myanmar Food"
    }
  ],
  "total": 2.5,
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Integration with Frontend

The frontend makes API calls to the `/api` endpoints, which are handled by the backend:

1. **Menu Page**: Fetches menu items from `/api/menu`
2. **Order Submission**: Sends order data to `/api/orders` (POST)
3. **Order History**: Fetches orders from `/api/orders` (GET)

## Running the Application

1. Start the backend server:
   ```bash
   # If using Docker
   docker-compose up
   
   # Or run directly
   python -m app.main
   ```

2. Start the frontend development server:
   ```bash
   cd ../react_frontend
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

## Troubleshooting

### Pydantic Import Error

If you encounter the error:
```
Import "pydantic" could not be resolved basedpyright(reportMissingImports)
```

This means the pydantic library is not installed. To fix this:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Or install pydantic directly:
   ```bash
   pip install pydantic
   ```

### CORS Issues

If the frontend cannot communicate with the backend, ensure that CORS is properly configured in the backend and that the frontend is making requests to the correct URL.

### Port Conflicts

Ensure that the backend is running on the expected port (typically 8000 or 8088) and that this matches the proxy configuration in the frontend.