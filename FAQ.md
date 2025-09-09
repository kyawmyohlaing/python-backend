# FastAPI Backend Template FAQ

Frequently Asked Questions about the FastAPI backend template.

## 📦 General Questions

### What is this FastAPI backend template?

This is a production-ready template for building web APIs with FastAPI. It includes:
- User authentication with JWT tokens
- Password hashing with bcrypt
- PostgreSQL database integration
- SQLAlchemy ORM
- Alembic database migrations
- Docker containerization
- Development and production configurations
- Example user seeding
- Comprehensive testing setup

### Why should I use this template?

This template provides a solid foundation for building scalable, secure web APIs with Python and FastAPI. It includes best practices for:
- Security (password hashing, JWT authentication)
- Database management (migrations, ORM)
- Containerization (Docker, Docker Compose)
- Development workflow (hot reload, testing)
- Project structure (separation of concerns)

### What are the system requirements?

- Docker and Docker Compose
- Git
- At least 4GB RAM (recommended)

### How do I customize this template for my project?

1. Clone the repository
2. Modify the models in `app/models/`
3. Update the schemas in `app/schemas/`
4. Add business logic in `app/services/`
5. Create new API endpoints in `app/routes/`
6. Update the database migrations
7. Customize the environment variables

## 🐳 Docker Questions

### How do I run the application in development mode?

```bash
make dev
```

This starts the application with hot reload enabled, so code changes are reflected immediately.

### How do I run the application in production mode?

```bash
make prod
```

This starts the application with Gunicorn workers for better performance.

### How do I stop the application?

```bash
make down
```

To also remove the database volume (losing all data):

```bash
make down -v
```

### Can I run the application without Docker?

Yes, but it requires manual setup:
1. Install Python 3.9+
2. Install PostgreSQL
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables
5. Run migrations: `alembic -c app/migrations/alembic.ini upgrade head`
6. Start the server: `uvicorn app.main:app --reload`

## 🔐 Authentication Questions

### How does authentication work?

1. Users register with email and password
2. Password is hashed using bcrypt before storage
3. Users login with email and password
4. Password is verified against the hashed version
5. JWT token is generated and returned
6. Client includes token in Authorization header for protected routes
7. Server validates token and extracts user information

### How do I register a new user?

Send a POST request to `/users/register` with:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

### How do I login?

Send a POST request to `/users/login` with:
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

The response will include an access token.

### How do I access protected routes?

Include the access token in the Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### How long do tokens last?

By default, tokens expire after 60 minutes. This can be configured with the `ACCESS_TOKEN_EXPIRE_MINUTES` environment variable.

### How do I change the secret key?

Set the `SECRET_KEY` environment variable in your `.env` file.

## 🗃️ Database Questions

### What database does this template use?

PostgreSQL is used by default, but the template can be adapted for other databases supported by SQLAlchemy.

### How do I run database migrations?

```bash
make migrate
```

Or manually:
```bash
docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head
```

### How do I create a new migration?

```bash
docker-compose exec web alembic -c app/migrations/alembic.ini revision --autogenerate -m "Description of changes"
```

### How do I add a new table?

1. Create a new model in `app/models/`
2. Create a migration:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini revision --autogenerate -m "Add new table"
   ```
3. Apply the migration:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head
   ```

### Is there sample data?

Yes, an example user is automatically created:
- Email: `user@example.com`
- Password: `password123`

## 🧪 Testing Questions

### How do I run tests?

```bash
make test
```

Or:
```bash
python -m pytest tests/
```

### What types of tests are included?

- Unit tests for user service functions
- Integration tests for API endpoints
- Tests for both SQLite (in-memory) and PostgreSQL

### How do I add new tests?

1. Create a new test file in the `tests/` directory
2. Follow the existing test patterns
3. Run tests to verify they work

### How do I run specific tests?

```bash
python -m pytest tests/test_users.py
python -m pytest tests/test_users.py::test_create_user
```

## 🛠️ Development Questions

### How do I add a new API endpoint?

1. Create a new route file in `app/routes/` or add to an existing one
2. Define the endpoint with appropriate decorators
3. Implement the business logic in `app/services/`
4. Add necessary models and schemas
5. Include the router in `app/main.py`

### How do I add a new dependency?

1. Add the dependency to `requirements.txt`
2. Rebuild the Docker image:
   ```bash
   docker-compose build
   ```

### How do I configure environment variables?

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit the `.env` file with your values

### How do I enable CORS?

Add CORS middleware to `app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚀 Deployment Questions

### How do I deploy this to production?

1. Update `docker-compose.yml` with production settings
2. Set secure environment variables
3. Use a reverse proxy like Nginx
4. Configure SSL certificates
5. Deploy to your hosting provider

### What hosting providers work well with this template?

- AWS (ECS, EKS, EC2)
- Google Cloud Platform (GKE, Compute Engine)
- Microsoft Azure (AKS, VMs)
- DigitalOcean
- Heroku (with container registry)
- Any provider that supports Docker

### How do I scale this application?

1. Increase Gunicorn worker count in Dockerfile
2. Use a load balancer
3. Scale the database separately
4. Add caching layers
5. Use a CDN for static assets

### How do I monitor this application?

1. Use Docker logging drivers
2. Implement application performance monitoring (APM)
3. Set up health check endpoints
4. Use external monitoring services
5. Implement custom metrics

## 🔧 Troubleshooting Questions

### What should I do if the application won't start?

1. Check the logs:
   ```bash
   docker-compose logs web
   docker-compose logs db
   ```
2. Verify environment variables
3. Check database connectivity
4. Ensure ports are not in use

### How do I reset the database?

```bash
make down -v  # This removes the database volume
make dev      # This recreates everything
```

### How do I update dependencies?

1. Update `requirements.txt`
2. Rebuild the Docker image:
   ```bash
   docker-compose build
   ```

### How do I backup the database?

```bash
docker-compose exec db pg_dump -U postgres mydb > backup.sql
```

## 📚 Learning Resources

### Where can I learn more about FastAPI?

- [Official FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI Video Course](https://fastapi.tiangolo.com/tutorial/)

### Where can I learn more about Docker?

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Tutorial](https://docs.docker.com/get-started/)

### Where can I learn more about PostgreSQL?

- [Official PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

## 🤝 Contributing

### How can I contribute to this template?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

### What kind of contributions are welcome?

- Bug fixes
- New features
- Documentation improvements
- Performance enhancements
- Security improvements
- Test coverage improvements

## 📄 License

### What license is this template under?

This template is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Can I use this template for commercial projects?

Yes, the MIT License allows for commercial use.