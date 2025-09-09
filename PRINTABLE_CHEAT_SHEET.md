# 📄 FastAPI Backend Template - Printable Cheat Sheet

---

## ⚡ Quick Start
```
cp .env.example .env
make dev
```

## 🚀 Main Commands
| Command | Action |
|---------|--------|
| `make dev` | Start development |
| `make prod` | Start production |
| `make down` | Stop containers |
| `make logs` | View logs |
| `make test` | Run tests |

## 🔐 Auth Flow
1. `POST /users/register` - Create account
2. `POST /users/login` - Get JWT token
3. `GET /users/me` - Access with `Authorization: Bearer <token>`

## 🧪 Test Examples

### Register
```
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"pass123"}'
```

### Login
```
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123"}'
```

### Access Protected
```
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐳 Docker
```
# Start
docker-compose up --build

# Stop
docker-compose down

# Migrate
docker-compose exec web alembic upgrade head
```

## 📂 Key Endpoints
- `POST /users/register` - Register user
- `POST /users/login` - Login user
- `GET /users/me` - Get current user
- `GET /users/` - List all users

## 🗃️ Example User
```
Email: user@example.com
Password: password123
```

## 🔗 URLs
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

*Keep this handy while developing!*