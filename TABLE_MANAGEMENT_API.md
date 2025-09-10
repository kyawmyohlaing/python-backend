# Table Management API Documentation

This document describes the Table Management API endpoints that allow for table assignment, seat tracking, and bill management.

## Base URL

All Table Management API endpoints are prefixed with `/api/tables`.

## Table Endpoints

### 1. Get All Tables

- **URL**: `/api/tables`
- **Method**: `GET`
- **Description**: Retrieve all tables in the restaurant
- **Response**:
  ```json
  [
    {
      "id": 1,
      "table_number": 1,
      "capacity": 4,
      "is_occupied": false,
      "current_order_id": null,
      "status": "available"
    }
  ]
  ```

### 2. Get Specific Table

- **URL**: `/api/tables/{table_id}`
- **Method**: `GET`
- **Description**: Retrieve a specific table by ID
- **Response**:
  ```json
  {
    "id": 1,
    "table_number": 1,
    "capacity": 4,
    "is_occupied": false,
    "current_order_id": null,
    "status": "available"
  }
  ```

### 3. Create New Table

- **URL**: `/api/tables`
- **Method**: `POST`
- **Description**: Create a new table
- **Request Body**:
  ```json
  {
    "table_number": 5,
    "capacity": 4
  }
  ```
- **Response**:
  ```json
  {
    "id": 5,
    "table_number": 5,
    "capacity": 4,
    "is_occupied": false,
    "current_order_id": null,
    "status": "available"
  }
  ```

### 4. Update Table

- **URL**: `/api/tables/{table_id}`
- **Method**: `PUT`
- **Description**: Update a table's information
- **Request Body**:
  ```json
  {
    "table_number": 5,
    "capacity": 6,
    "is_occupied": true,
    "current_order_id": 1,
    "status": "occupied"
  }
  ```
- **Response**:
  ```json
  {
    "id": 5,
    "table_number": 5,
    "capacity": 6,
    "is_occupied": true,
    "current_order_id": 1,
    "status": "occupied"
  }
  ```

### 5. Delete Table

- **URL**: `/api/tables/{table_id}`
- **Method**: `DELETE`
- **Description**: Delete a table (only if not occupied)
- **Response**:
  ```json
  {
    "message": "Table deleted successfully"
  }
  ```

## Table Status Management Endpoints

### 1. Assign Table to Order

- **URL**: `/api/tables/{table_id}/assign/{order_id}`
- **Method**: `POST`
- **Description**: Assign a table to an order
- **Response**:
  ```json
  {
    "id": 1,
    "table_number": 1,
    "capacity": 4,
    "is_occupied": true,
    "current_order_id": 1,
    "status": "occupied"
  }
  ```

### 2. Release Table

- **URL**: `/api/tables/{table_id}/release`
- **Method**: `POST`
- **Description**: Release a table (mark as available)
- **Response**:
  ```json
  {
    "id": 1,
    "table_number": 1,
    "capacity": 4,
    "is_occupied": false,
    "current_order_id": null,
    "status": "available"
  }
  ```

## Table Status Filtering Endpoints

### 1. Get Occupied Tables

- **URL**: `/api/tables/occupied`
- **Method**: `GET`
- **Description**: Retrieve all occupied tables
- **Response**:
  ```json
  [
    {
      "id": 1,
      "table_number": 1,
      "capacity": 4,
      "is_occupied": true,
      "current_order_id": 1,
      "status": "occupied"
    }
  ]
  ```

### 2. Get Available Tables

- **URL**: `/api/tables/available`
- **Method**: `GET`
- **Description**: Retrieve all available tables
- **Response**:
  ```json
  [
    {
      "id": 2,
      "table_number": 2,
      "capacity": 2,
      "is_occupied": false,
      "current_order_id": null,
      "status": "available"
    }
  ]
  ```

## Order Integration

### 1. Create Order with Table Assignment

- **URL**: `/api/orders`
- **Method**: `POST`
- **Description**: Create a new order and automatically assign it to a table
- **Request Body**:
  ```json
  {
    "order": [
      {
        "name": "Shan Noodles",
        "price": 2.5,
        "category": "Myanmar Food"
      }
    ],
    "total": 2.5,
    "table_id": 1,
    "customer_count": 2,
    "special_requests": "Extra spicy"
  }
  ```
- **Response**:
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
    "table_id": 1,
    "customer_count": 2,
    "special_requests": "Extra spicy",
    "timestamp": "2023-01-01T00:00:00Z"
  }
  ```

### 2. Update Order Table Assignment

- **URL**: `/api/orders/{order_id}`
- **Method**: `PUT`
- **Description**: Update an order's table assignment
- **Request Body**:
  ```json
  {
    "table_id": 2
  }
  ```
- **Response**:
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
    "table_id": 2,
    "customer_count": 2,
    "special_requests": "Extra spicy",
    "timestamp": "2023-01-01T00:00:00Z"
  }
  ```

## Table Status Values

- `available` - Table is available for seating
- `occupied` - Table is currently occupied
- `reserved` - Table is reserved for future seating
- `cleaning` - Table is being cleaned

## Integration with Frontend

The Table Management API can be integrated with the frontend to provide:

1. **Table View**: Visual representation of restaurant tables
2. **Table Assignment**: Assign tables to new orders
3. **Table Release**: Release tables when orders are completed
4. **Table Status Tracking**: Real-time tracking of table availability
5. **Customer Count Management**: Track number of customers per table
6. **Special Requests**: Capture and display special customer requests

## Example Usage

### Fetching All Tables
```javascript
// Fetch all tables
const response = await fetch('/api/tables');
const tables = await response.json();
```

### Assigning a Table to an Order
```javascript
// Assign table 1 to order 1
const response = await fetch('/api/tables/1/assign/1', {
  method: 'POST',
});
const updatedTable = await response.json();
```

### Releasing a Table
```javascript
// Release table 1
const response = await fetch('/api/tables/1/release', {
  method: 'POST',
});
const updatedTable = await response.json();
```

## Error Handling

All API endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (e.g., table already occupied, invalid data)
- `404`: Not Found (e.g., table or order not found)
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```