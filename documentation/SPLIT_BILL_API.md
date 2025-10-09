# Split Bill API Documentation

## Overview
The split bill functionality allows restaurant staff to divide a single order into multiple separate orders based on different criteria such as items, seats, or equal distribution.

## Endpoint
```
POST /api/tables/{table_id}/split-bill
```

## Methods

### 1. Split by Items
Split the bill by specific items in the order.

**Request Body:**
```json
{
  "method": "items",
  "splits": [
    {
      "items": [0, 1]  // Indices of items in the original order
    },
    {
      "items": [2, 3]  // Indices of items in the original order
    }
  ]
}
```

### 2. Split by Seats
Split the bill by assigning items to specific seats.

**Request Body:**
```json
{
  "method": "seats",
  "seat_assignments": {
    "1": [0, 1],  // Seat 1 gets items at indices 0 and 1
    "2": [2, 3]   // Seat 2 gets items at indices 2 and 3
  }
}
```

### 3. Split Equally
Split the bill into equal parts.

**Request Body:**
```json
{
  "method": "equal",
  "parts": 2  // Number of equal parts to split into
}
```

## Response
The API returns an array of new OrderResponse objects, each representing a split portion of the original order.

## Example Usage
```javascript
// Split by items
const response = await fetch(`/api/tables/1/split-bill`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    method: "items",
    splits: [
      { items: [0, 1] },
      { items: [2, 3] }
    ]
  })
});
```

## Error Handling
- 404: Table not found
- 400: Table not occupied or invalid split method
- 404: Order not found