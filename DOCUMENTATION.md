# API Documentation

This document provides a comprehensive overview of all available API endpoints in the FastAPI backend.

## Base URL

All API endpoints are prefixed with `/api`.

## Authentication

Most endpoints require authentication via JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Menu API Endpoints

### 1. Get All Menu Items

- **URL**: `/api/menu/`
- **Method**: `GET`
- **Description**: Retrieve all menu items
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Shan Noodles",
      "price": 2.5,
      "category": "Myanmar Food"
    }
  ]
  ```

### 2. Create a Menu Item

- **URL**: `/api/menu/`
- **Method**: `POST`
- **Description**: Create a new menu item
- **Request Body**:
  ```json
  {
    "name": "New Item",
    "price": 5.99,
    "category": "New Category"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "New Item",
    "price": 5.99,
    "category": "New Category"
  }
  ```

### 3. Create Multiple Menu Items (Batch)

- **URL**: `/api/menu/batch`
- **Method**: `POST`
- **Description**: Create multiple menu items in a single request
- **Request Body**:
  ```json
  [
    {
      "name": "Item 1",
      "price": 1.99,
      "category": "Category 1"
    },
    {
      "name": "Item 2",
      "price": 2.99,
      "category": "Category 2"
    }
  ]
  ```
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Item 1",
      "price": 1.99,
      "category": "Category 1"
    },
    {
      "id": 2,
      "name": "Item 2",
      "price": 2.99,
      "category": "Category 2"
    }
  ]
  ```

### 4. Get a Specific Menu Item

- **URL**: `/api/menu/{item_id}`
- **Method**: `GET`
- **Description**: Retrieve a specific menu item by ID
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Shan Noodles",
    "price": 2.5,
    "category": "Myanmar Food"
  }
  ```

### 5. Update a Menu Item

- **URL**: `/api/menu/{item_id}`
- **Method**: `PUT`
- **Description**: Update an existing menu item
- **Request Body**:
  ```json
  {
    "name": "Updated Name",
    "price": 3.5,
    "category": "Updated Category"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Updated Name",
    "price": 3.5,
    "category": "Updated Category"
  }
  ```

### 6. Delete a Menu Item

- **URL**: `/api/menu/{item_id}`
- **Method**: `DELETE`
- **Description**: Delete a menu item
- **Response**:
  ```json
  {
    "message": "Menu item deleted successfully"
  }
  ```

### 7. Get Menu Items by Category

- **URL**: `/api/menu/category/{category}`
- **Method**: `GET`
- **Description**: Retrieve all menu items in a specific category
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Shan Noodles",
      "price": 2.5,
      "category": "Myanmar Food"
    }
  ]
  ```

### 8. Get All Menu Categories

- **URL**: `/api/menu/categories`
- **Method**: `GET`
- **Description**: Retrieve all unique menu categories
- **Response**:
  ```json
  [
    "Myanmar Food",
    "Western Food",
    "Beverages",
    "Desserts"
  ]
  ```

## Error Responses

All API endpoints return appropriate HTTP status codes:
- `200`: Success
- `201`: Created (for POST requests)
- `400`: Bad Request (validation errors, duplicates, etc.)
- `401`: Unauthorized (authentication required)
- `404`: Not Found
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```