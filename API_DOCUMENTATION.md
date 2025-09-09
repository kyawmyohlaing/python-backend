# FastAPI Backend Template API Documentation

This document describes the API endpoints available in the FastAPI backend template.

## 🏠 Base URL

All endpoints are relative to: `http://localhost:8000`

## 🔌 Endpoints

### User Registration

**POST** `/users/register`

Register a new user.

#### Request Body
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

#### Response
```json
{
  "id": 0,
  "name": "string",
  "email": "string"
}
```

#### Errors
- 400: Email already registered

---

### User Login

**POST** `/users/login`

Authenticate a user and receive a JWT token.

#### Request Body
```json
{
  "email": "string",
  "password": "string"
}
```

#### Response
```json
{
  "access_token": "string",
  "token_type": "string"
}
```

#### Errors
- 401: Invalid email or password

---

### Get Current User

**GET** `/users/me`

Get information about the currently authenticated user.

#### Headers
```http
Authorization: Bearer <token>
```

#### Response
```json
{
  "id": 0,
  "name": "string",
  "email": "string"
}
```

#### Errors
- 401: Invalid token or user not found

---

### List All Users

**GET** `/users/`

Get a list of all registered users.

#### Headers
```http
Authorization: Bearer <token>
```

#### Response
```json
[
  {
    "id": 0,
    "name": "string",
    "email": "string"
  }
]
```

---

## 🔐 Authentication

Most endpoints require authentication using JWT tokens. To authenticate, include the following header in your requests:

```http
Authorization: Bearer <your_token_here>
```

Tokens are obtained by successfully logging in via the `/users/login` endpoint.

## 📦 Data Models

### UserCreate
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

### UserResponse
```json
{
  "id": 0,
  "name": "string",
  "email": "string"
}
```

### UserLogin
```json
{
  "email": "string",
  "password": "string"
}
```

### Token
```json
{
  "access_token": "string",
  "token_type": "string"
}
```

## 🛠️ Using the API

### With cURL

#### Register a new user
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "password123"}'
```

#### Login
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}'
```

#### Get current user (replace `YOUR_TOKEN_HERE` with actual token)
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### With Python Requests

```python
import requests

# Register a new user
response = requests.post('http://localhost:8000/users/register', json={
    'name': 'John Doe',
    'email': 'john@example.com',
    'password': 'password123'
})
print(response.json())

# Login
response = requests.post('http://localhost:8000/users/login', json={
    'email': 'john@example.com',
    'password': 'password123'
})
token = response.json()['access_token']

# Get current user
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/users/me', headers=headers)
print(response.json())
```

## 🧪 Testing

The API can be tested using the built-in Swagger UI documentation available at `http://localhost:8000/docs` when the server is running.

## 🔒 Security

- All passwords are hashed using bcrypt before storage
- JWT tokens are signed using HS256 algorithm
- Passwords are never returned in API responses
- Email uniqueness is enforced at the database level