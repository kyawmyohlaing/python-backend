# 🚀 FastAPI Backend Cheat Sheet

## 🏁 Quick Start

```bash
# Setup
cp .env.example .env
make dev

# Or with Docker
docker-compose up --build
```

## 🔧 Development Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start development server |
| `make prod` | Start production server |
| `make test` | Run all tests |
| `make migrate` | Run database migrations |
| `make logs` | View application logs |
| `make clean` | Clean temporary files |

## 🌐 API Access

- API: `http://localhost:8088`
- Docs: `http://localhost:8088/docs`
- Redoc: `http://localhost:8088/redoc`

## 🔐 Authentication

### Register New User
```
POST /users/register
```
**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Login
```
POST /users/login
```
**Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User (JWT Protected)
```
GET /users/me
```
**Header:**
```
Authorization: Bearer <access_token>
```
**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### List All Users
```
GET /users/
```
**Header:**
```
Authorization: Bearer <access_token>
```

## 🧪 Testing

### With cURL
```bash
# Register
curl -X POST http://localhost:8088/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
  }'

# Login
curl -X POST http://localhost:8088/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword"
  }'

# Get current user (replace TOKEN with actual token)
curl http://localhost:8088/users/me \
  -H "Authorization: Bearer TOKEN"
```

### With Python
```python
import requests

# Register
response = requests.post('http://localhost:8088/users/register', json={
    'name': 'John Doe',
    'email': 'john@example.com',
    'password': 'securepassword'
})

# Login
response = requests.post('http://localhost:8088/users/login', json={
    'email': 'john@example.com',
    'password': 'securepassword'
})
token = response.json()['access_token']

# Get current user
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8088/users/me', headers=headers)
```

## 🐳 Docker Commands

```bash
# Development (with hot reload)
docker-compose up

# Production
docker-compose -f docker-compose.yml up

# Stop services
docker-compose down

# View logs
docker-compose logs

# Run migrations
docker-compose exec web alembic upgrade head

# Access container shell
docker-compose exec web bash
```

## 📁 Project Structure

```
app/
├── main.py          # Application entry point
├── config.py        # Configuration management
├── database.py      # Database connection setup
├── security.py      # Authentication and password hashing
├── models/          # Database models (SQLAlchemy)
├── schemas/         # Data validation models (Pydantic)
├── routes/          # API endpoints (FastAPI)
├── services/        # Business logic
├── utils/           # Utility functions
├── migrations/      # Database migration scripts
tests/               # Unit and integration tests
```

## 🛠️ Environment Variables

Create a `.env` file with:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🔧 Troubleshooting

### Common Issues
1. **Port in use**: Change ports in `docker-compose.yml`
2. **Database connection**: Check `DATABASE_URL` in `.env`
3. **Migration errors**: Run `make migrate` or check migration files
4. **Permission errors**: Ensure Docker has proper permissions

### Reset Database
```bash
# Stop services
docker-compose down -v

# Start fresh
docker-compose up --build
```