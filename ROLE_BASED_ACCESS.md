# Role-Based Access Control (RBAC)

This document describes the role-based access control system implemented in the FastAPI backend.

## Available Roles

The system supports the following user roles:

1. **admin** - Full system access
2. **manager** - Management functions access
3. **waiter** - Order taking and table management
4. **cashier** - Payment processing
5. **chef** - Kitchen order management
6. **kitchen** - Kitchen staff functions
7. **bar** - Bar staff functions

## User Registration with Roles

When registering a new user, you can specify their role. If no role is provided, the default role is "waiter".

### API Endpoint

```
POST /users/register
```

### Request Body

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "manager"
}
```

### Response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "manager"
}
```

## Role-Based Access Control in Code

The system provides dependencies for enforcing role-based access control in your API endpoints.

### Require Specific Role

```python
from fastapi import Depends
from app.dependencies import require_role
from app.schemas.user_schema import UserRole

@app.get("/manager-only")
def manager_endpoint(current_user: User = Depends(require_role(UserRole.MANAGER))):
    return {"message": "Only managers can access this endpoint"}
```

### Require Any of Multiple Roles

```python
from fastapi import Depends
from app.dependencies import require_any_role
from app.schemas.user_schema import UserRole

@app.get("/staff-only")
def staff_endpoint(current_user: User = Depends(require_any_role([UserRole.MANAGER, UserRole.WAITER, UserRole.CASHIER]))):
    return {"message": "Only staff members can access this endpoint"}
```

## Sample Users

The system includes the following sample users for testing:

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin | admin@example.com | admin123 | admin |
| manager | manager@example.com | manager123 | manager |
| waiter | waiter@example.com | waiter123 | waiter |
| cashier | cashier@example.com | cashier123 | cashier |
| chef | chef@example.com | chef123 | chef |

## Testing Role-Based Access

You can test the role-based access control using the provided test script:

```bash
python examples/role_based_access.py
```

Or run the unit tests:

```bash
pytest tests/test_user_roles.py
```