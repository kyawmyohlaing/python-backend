# 🚀 FastAPI Backend - Quick Reference

## 🏁 Getting Started
```bash
# Setup
cp .env.example .env
make dev

# Test with example user
# Email: user@example.com
# Password: password123
```

## 🛠️ Development Commands
```bash
make dev      # Development (hot reload)
make prod     # Production (Gunicorn)
make down     # Stop containers
make logs     # View logs
make migrate  # Run migrations
make test     # Run tests
```

## 🔐 Authentication Flow

1. **Register** → `POST /users/register`
2. **Login** → `POST /users/login` → JWT Token
3. **Access** → `GET /users/me` with `Authorization: Bearer <token>`

## 🧪 API Testing

### Register User
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"pass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123"}'
```

### Access Protected Route
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🐳 Docker Commands
```bash
# Build and start
docker-compose up --build

# Stop
docker-compose down

# Run migrations
docker-compose exec web alembic upgrade head

# Access container
docker-compose exec web bash
```

## 📁 Key Files
- `app/main.py` - App entry point
- `app/models/user.py` - User model
- `app/schemas/user_schema.py` - Data validation
- `app/services/user_service.py` - Business logic
- `app/routes/user_routes.py` - API endpoints
- `app/security.py` - Auth functions
- `Dockerfile` - Production config
- `requirements.txt` - Dependencies

## 🗃️ Database
- **Seeded User**: user@example.com / password123
- **Migrations**: `app/migrations/versions/`
- **Alembic**: Auto-runs on startup

## 🔗 URLs
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc