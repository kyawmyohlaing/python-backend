# ⚡ FastAPI Backend Template Cheat Sheet

## 🚀 Quick Command Reference

### Makefile Commands
| Command        | Purpose                                        |
| -------------- | ---------------------------------------------- |
| `make dev`     | Start development (Uvicorn + hot reload)       |
| `make prod`    | Start production (Gunicorn workers)            |
| `make down`    | Stop all containers                            |
| `make logs`    | Tail web container logs                        |
| `make migrate` | Run Alembic migrations manually                |
| `make test`    | Run all tests                                  |

### Docker Commands
| Command                                                                      | Description                |
| ---------------------------------------------------------------------------- | -------------------------- |
| `docker-compose up --build`                                                  | Build and start containers |
| `docker-compose down`                                                        | Stop containers            |
| `docker-compose down -v`                                                     | Stop and remove volumes    |
| `docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head` | Apply migrations           |
| `docker-compose logs web`                                                    | View web service logs      |
| `docker-compose exec web bash`                                               | Access web container shell |

## 🔐 API Routes

### User Registration
```
POST /users/register
```
**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

### User Login
```
POST /users/login
```
**Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
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
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}'

# Get current user (replace TOKEN with actual token)
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer TOKEN"
```

### With Python
```python
import requests

# Register
response = requests.post('http://localhost:8000/users/register', json={
    'name': 'John Doe',
    'email': 'john@example.com',
    'password': 'password123'
})

# Login
response = requests.post('http://localhost:8000/users/login', json={
    'email': 'john@example.com',
    'password': 'password123'
})
token = response.json()['access_token']

# Get current user
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/users/me', headers=headers)
```

## 🗃️ Database & Migrations

### Alembic Commands
```bash
# Create new migration
docker-compose exec web alembic -c app/migrations/alembic.ini revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head

# Check current revision
docker-compose exec web alembic -c app/migrations/alembic.ini current

# View migration history
docker-compose exec web alembic -c app/migrations/alembic.ini history
```

## 🐳 Environment

### Seeded Example User
```
Email: user@example.com
Password: password123
```

### Key URLs
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## 🛠️ Development

### Project Structure
```
fastapi-backend-template/
├── app/
│   ├── models/     # Database models
│   ├── schemas/    # Pydantic schemas
│   ├── services/   # Business logic
│   ├── routes/     # API endpoints
│   └── migrations/ # Database migrations
├── tests/          # Test suite
├── Dockerfile      # Production Docker config
└── docker-compose.yml  # Services config
```

### Key Files
- `app/main.py` - Application entry point
- `app/database.py` - Database configuration
- `app/security.py` - Authentication & security
- `requirements.txt` - Python dependencies
- `Makefile` - Development commands
- `.env.example` - Environment variables template

## 🔧 Troubleshooting

### Common Issues
1. **Port in use**: Change ports in `docker-compose.yml`
2. **Database connection**: Check `DATABASE_URL` in `.env`
3. **Migration errors**: Run `make migrate` or check migration files
4. **Permission errors**: Ensure Docker has proper permissions

### Reset Database
```bash
make down -v  # Remove volumes
make dev      # Recreate everything
```