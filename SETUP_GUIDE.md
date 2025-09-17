# FastAPI Backend Template Setup Guide

This guide will help you set up and customize the FastAPI backend template for your project.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Docker and Docker Compose
- Git

## 🚀 Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/fastapi-backend-template.git
   cd fastapi-backend-template
   ```

2. **Copy the environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Generate a secure SECRET_KEY:**
   The template includes a script to generate cryptographically secure keys:
   ```bash
   python generate_secret.py
   ```
   
   Copy the generated key and set it as your `SECRET_KEY` in the `.env` file.

4. **Review and customize environment variables in `.env`:**
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: ⚠️ **Critical** - Must be a unique, secure secret key
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## ▶️ Running the Application

### Development Mode (with hot reload)
```bash
make dev
```

This command:
- Builds the Docker images
- Starts the PostgreSQL database
- Starts the FastAPI application with Uvicorn and hot reload
- Automatically runs Alembic migrations
- Seeds the example user

### Production Mode (with Gunicorn)
```bash
make prod
```

This command:
- Builds the Docker images
- Starts the PostgreSQL database
- Starts the FastAPI application with Gunicorn workers
- Automatically runs Alembic migrations
- Seeds the example user

## 🧪 Testing the API

Once the application is running, you can test the endpoints:

### 1. Login with the Example User
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Access Protected Route
Extract the `access_token` from the login response and use it:
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 3. Register a New User
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "securepassword"}'
```

### 4. Login with the New User
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "securepassword"}'
```

## 🔐 Security Best Practices

### Generating Secure Keys

For production deployments, always generate unique, secure keys for each environment:

1. **Development Environment:**
   ```bash
   python generate_secret.py
   ```
   Copy the output and use it as your `SECRET_KEY` in `.env`

2. **Production Environment:**
   Generate a new key and store it securely (never in version control):
   ```bash
   python generate_secret.py
   ```

3. **Testing Environment:**
   Use a different generated key for testing to ensure isolation.

### Key Management

- Never commit secret keys to version control
- Use different keys for development, testing, and production
- Rotate keys periodically
- Store production keys in secure secret management systems

## 🛠️ Customization

### Adding New Models
1. Create a new file in `app/models/`
2. Define your SQLAlchemy model
3. Create an Alembic migration:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini revision --autogenerate -m "Add new model"
   ```
4. Apply the migration:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head
   ```

### Adding New Schemas
1. Create a new file in `app/schemas/`
2. Define your Pydantic models

### Adding New Services
1. Create a new file in `app/services/`
2. Implement your business logic

### Adding New Routes
1. Create a new file in `app/routes/`
2. Define your API endpoints
3. Include the router in `app/main.py`

## 🗃️ Database Management

### Running Migrations
```bash
make migrate
```
or
```bash
docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head
```

### Creating New Migrations
```bash
docker-compose exec web alembic -c app/migrations/alembic.ini revision --autogenerate -m "Description of changes"
```

### Seeding Data
To add more seed data, create new migration files in `app/migrations/versions/` following the pattern in `0002_seed_user.py`.

### Database Connection Testing

To verify your database connection is properly configured, run the test script:
```bash
python test_db_connection.py
```

This script will:
- Check if your `.env` file is properly configured
- Test the database connection using your configured credentials
- Provide specific troubleshooting advice if the connection fails

## 🧪 Running Tests

### Run All Tests
```bash
make test
```
or
```bash
python -m pytest tests/
```

### Run Specific Tests
```bash
python -m pytest tests/test_users.py
```

## 🛑 Stopping the Application

To stop all containers:
```bash
make down
```

To stop and remove volumes (including database data):
```bash
make down -v
```

## 📊 Monitoring

### View Logs
```bash
make logs
```

### View Specific Service Logs
```bash
docker-compose logs web
docker-compose logs db
```

## 🧰 Additional Tools

### Generate New Secret Key
```bash
python generate_secret.py
```

This script generates a cryptographically secure random key suitable for use as a SECRET_KEY.

## 🔧 Troubleshooting

### Common Issues

1. **Port already in use:**
   - Change the port in `docker-compose.yml` or stop the conflicting service

2. **Database connection errors:**
   - Ensure the database service is running
   - Check the `DATABASE_URL` in your `.env` file
   - Run `python test_db_connection.py` for detailed diagnostics

3. **Migration errors:**
   - Check the migration files in `app/migrations/versions/`
   - Ensure the database is accessible

4. **Permission errors:**
   - Ensure Docker has the necessary permissions
   - On Linux, you might need to run with `sudo`

### Resetting the Database
If you need to start with a fresh database:
```bash
make down -v  # This removes the database volume
make dev      # This recreates the database and runs migrations
```

## 🚀 Deployment