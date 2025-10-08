# Analytics API Documentation

## Overview

This document describes the Analytics API endpoints implemented for the restaurant POS system. These endpoints provide insights into top-selling items and peak business hours to help managers make data-driven decisions.

## Base URL

All endpoints are prefixed with `/api/analytics`

## Authentication

All endpoints require authentication using a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Get Top Selling Items

#### Request
```
GET /api/analytics/reports/top-items
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string (ISO 8601) | No | Start date for filtering (default: 30 days ago) |
| end_date | string (ISO 8601) | No | End date for filtering (default: current date) |
| limit | integer | No | Number of items to return (default: 10, min: 1, max: 100) |

#### Response
```json
{
  "items": [
    {
      "name": "Item Name",
      "category": "Item Category",
      "quantity": 25,
      "revenue": 125.50,
      "average_price": 5.02
    }
  ]
}
```

#### Example
```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/top-items?limit=5&start_date=2023-01-01&end_date=2023-01-31"
```

### 2. Get Peak Hours

#### Request
```
GET /api/analytics/reports/peak-hours
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string (ISO 8601) | No | Start date for filtering (default: 30 days ago) |
| end_date | string (ISO 8601) | No | End date for filtering (default: current date) |

#### Response
```json
{
  "hours": [
    {
      "hour": 12,
      "order_count": 15,
      "total_revenue": 320.75,
      "average_order_value": 21.38
    }
  ]
}
```

#### Example
```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/peak-hours?start_date=2023-01-01&end_date=2023-01-31"
```

### 3. Get Daily Sales Report

#### Request
```
GET /api/analytics/reports/daily
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string (ISO 8601) | No | Start date for filtering (default: 30 days ago) |
| end_date | string (ISO 8601) | No | End date for filtering (default: current date) |

#### Response
```json
{
  "period": "2023-01-01 to 2023-01-31",
  "start_date": "2023-01-01",
  "end_date": "2023-01-31",
  "total_sales": 12500.75,
  "total_orders": 425,
  "average_daily_sales": 403.25,
  "sales_data": [
    {
      "date": "2023-01-01",
      "total_sales": 1250.50,
      "order_count": 42,
      "total_items": 85,
      "average_order_value": 29.77
    }
  ]
}
```

#### Example
```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/daily?start_date=2023-01-01&end_date=2023-01-31"
```

### 4. Get Weekly Sales Report

#### Request
```
GET /api/analytics/reports/weekly
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string (ISO 8601) | No | Start date for filtering (default: 30 days ago) |
| end_date | string (ISO 8601) | No | End date for filtering (default: current date) |

#### Response
```json
{
  "period": "2023-01-01 to 2023-01-31",
  "start_date": "2023-01-01",
  "end_date": "2023-01-31",
  "total_sales": 12500.75,
  "total_orders": 425,
  "average_weekly_sales": 2500.15,
  "sales_data": [
    {
      "date": "2023-01-01",
      "total_sales": 2500.50,
      "order_count": 85,
      "total_items": 170,
      "average_order_value": 29.42
    }
  ]
}
```

#### Example
```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/weekly?start_date=2023-01-01&end_date=2023-01-31"
```

### 5. Get Monthly Sales Report

#### Request
```
GET /api/analytics/reports/monthly
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string (ISO 8601) | No | Start date for filtering (default: 30 days ago) |
| end_date | string (ISO 8601) | No | End date for filtering (default: current date) |

#### Response
```json
{
  "period": "2023-01-01 to 2023-01-31",
  "start_date": "2023-01-01",
  "end_date": "2023-01-31",
  "total_sales": 12500.75,
  "total_orders": 425,
  "average_monthly_sales": 12500.75,
  "sales_data": [
    {
      "date": "2023-01-01",
      "total_sales": 12500.75,
      "order_count": 425,
      "total_items": 850,
      "average_order_value": 29.41
    }
  ]
}
```

#### Example
```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/monthly?start_date=2023-01-01&end_date=2023-01-31"
```

## Error Responses

All endpoints may return the following error responses:

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Implementation Details

### Data Processing Logic

#### Top Selling Items
1. Aggregate all order items within the date range
2. Group by item name
3. Calculate total quantity sold and revenue per item
4. Compute average price per item
5. Sort by quantity sold (descending)
6. Limit to top N items (default 10)

#### Peak Hours
1. Extract hour component from order timestamps
2. Group orders by hour
3. Calculate order count and total revenue per hour
4. Compute average order value per hour
5. Sort by hour for chronological display

### Database Queries

The endpoints query the Order model from the database:
- Filter orders by timestamp within the specified date range
- Process order items to calculate analytics metrics
- Return structured JSON responses

## Testing

To test the endpoints, you can use the following curl commands (replace `<token>` with a valid JWT token):

```bash
# Get top selling items
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/top-items"

# Get peak hours
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/peak-hours"

# Get daily sales report
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/daily"

# Get weekly sales report
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/weekly"

# Get monthly sales report
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/analytics/reports/monthly"
```

## Integration with Frontend

The frontend analytics component expects the following data structures:

### Top Selling Items Response
```typescript
interface TopSellingItem {
  name: string;
  category: string;
  quantity: number;
  revenue: number;
  average_price: number;
}

interface TopSellingItemsResponse {
  items: TopSellingItem[];
}
```

### Peak Hours Response
```typescript
interface PeakHour {
  hour: number;
  order_count: number;
  total_revenue: number;
  average_order_value: number;
}

interface PeakHoursResponse {
  hours: PeakHour[];
}
```

## Future Enhancements

1. **Additional Analytics**:
   - Customer demographics analysis
   - Order type distribution
   - Revenue trends over time

2. **Advanced Filtering**:
   - Filter by order type (dine-in, takeaway, delivery)
   - Filter by specific menu categories
   - Compare periods (week-over-week, month-over-month)

3. **Enhanced Visualizations**:
   - Interactive charts with drill-down capabilities
   - Heatmaps for peak hours
   - Trend lines for top-selling items

4. **Real-time Analytics**:
   - Live updating dashboards
   - Alert notifications for business milestones
   - Performance benchmarks