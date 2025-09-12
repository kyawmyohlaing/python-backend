# Kitchen API Documentation

This document describes the Kitchen API endpoints that allow kitchen staff to view and manage orders.

## Base URL

All Kitchen API endpoints are prefixed with `/api/kitchen`.

## Endpoints

### 1. Get Kitchen Orders

- **URL**: `/api/kitchen/orders`
- **Method**: `GET`
- **Description**: Retrieve all orders that are currently in the kitchen for preparation
- **Response**:
  ```json
  [
    {
      "id": 1,
      "order_id": 1,
      "status": "pending",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "order_items": [
        {
          "name": "Shan Noodles",
          "price": 2.5,
          "category": "Myanmar Food"
        }
      ],
      "total": 2.5
    }
  ]
  ```

### 2. Create Kitchen Order

- **URL**: `/api/kitchen/orders`
- **Method**: `POST`
- **Description**: Add a new order to the kitchen display
- **Request Body**:
  ```json
  {
    "order_id": 1,
    "status": "pending"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "order_id": 1,
    "status": "pending",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```

### 3. Update Kitchen Order Status

- **URL**: `/api/kitchen/orders/{order_id}`
- **Method**: `PUT`
- **Description**: Update the status of an order in the kitchen
- **Request Body**:
  ```json
  {
    "status": "preparing"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "order_id": 1,
    "status": "preparing",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:01:00Z"
  }
  ```

### 4. Remove Kitchen Order

- **URL**: `/api/kitchen/orders/{order_id}`
- **Method**: `DELETE`
- **Description**: Remove an order from the kitchen display (when it's completed and served)
- **Response**:
  ```json
  {
    "message": "Order removed from kitchen display"
  }
  ```

### 5. Mark Order as Served

- **URL**: `/api/kitchen/orders/{order_id}/mark-served`
- **Method**: `POST`
- **Description**: Mark an order as served and update its status in the kitchen
- **Response**:
  ```json
  {
    "message": "Order marked as served",
    "order_id": 1,
    "status": "served"
  }
  ```

## Order Status Values

- `pending` - Order has been received but not yet started
- `preparing` - Kitchen staff are preparing the order
- `ready` - Order is ready to be served
- `served` - Order has been delivered to the customer

## Status Flow

Orders progress through statuses in the following flow:
```
pending → preparing → ready → served
```

## Integration with Frontend

The Kitchen API can be integrated with a kitchen display system that shows:

1. **Real-time Order Updates**: New orders automatically appear in the kitchen display
2. **Order Status Management**: Kitchen staff can update the status of orders as they progress
3. **Order Completion**: Completed orders are marked as served and resources are released

## Example Usage

### Fetching Kitchen Orders
```javascript
// Fetch all orders for the kitchen
const response = await fetch('/api/kitchen/orders');
const kitchenOrders = await response.json();
```

### Updating Order Status
```javascript
// Update an order status to "preparing"
const response = await fetch('/api/kitchen/orders/1', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ status: 'preparing' }),
});
const updatedOrder = await response.json();
```

### Marking Order as Served
```javascript
// Mark an order as served
const response = await fetch('/api/kitchen/orders/1/mark-served', {
  method: 'POST',
});
const result = await response.json();
```

### Removing Completed Order
```javascript
// Remove a completed order from the kitchen display
const response = await fetch('/api/kitchen/orders/1', {
  method: 'DELETE',
});
const result = await response.json();
```

## Error Handling

All API endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```