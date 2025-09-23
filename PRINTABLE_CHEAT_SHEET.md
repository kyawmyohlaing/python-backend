# 🚀 FastAPI Backend - Printable Cheat Sheet

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

## 🔐 Auth Flow
1. `POST /users/register` - Create account
2. `POST /users/login` - Get JWT token
3. `GET /users/me` - Access with `Authorization: Bearer <token>`

## 🧪 Test Examples

### Register User
```bash
curl -X POST http://localhost:8088/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"pass123"}'
```

### Login
```bash
curl -X POST http://localhost:8088/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123"}'
```

### Access Protected Route
```bash
curl http://localhost:8088/users/me \
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

## 🔧 Environment Variables
```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/db
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🌐 API Access
- API: `http://localhost:8088`
- Docs: `http://localhost:8088/docs`
- Redoc: `http://localhost:8088/redoc`