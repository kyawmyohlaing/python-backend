# Database Setup and Management

## 🐘 PostgreSQL Setup

1. Install PostgreSQL on your system
2. Create a database:
```sql
CREATE DATABASE mydb;
```
3. Create a user:
```sql
CREATE USER postgres WITH PASSWORD 'password';
```
4. Grant privileges:
```sql
GRANT ALL PRIVILEGES ON DATABASE mydb TO postgres;
```

## ⚙️ Environment Configuration

The database connection is configured through the `.env` file:

```ini
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
```

## 🗃️ Alembic Migrations

Alembic is used for database migrations. The migrations are stored in `app/migrations/versions/`.

### Creating a New Migration

1. Make changes to your models in `app/models/`
2. Generate a migration:
```bash
alembic -c app/migrations/alembic.ini revision --autogenerate -m "description of changes"
```

### Applying Migrations

To apply all pending migrations:
```bash
alembic -c app/migrations/alembic.ini upgrade head
```

### Rolling Back Migrations

To roll back the last migration:
```bash
alembic -c app/migrations/alembic.ini downgrade -1
```

## 🏗️ Initial Setup

1. Ensure PostgreSQL is running
2. Create the database and user as described above
3. Update the `.env` file with your database credentials
4. Run the initial migration:
```bash
alembic -c app/migrations/alembic.ini upgrade head
```

## 🔍 Migration Commands

- `alembic -c app/migrations/alembic.ini current` - Show current revision
- `alembic -c app/migrations/alembic.ini history` - Show migration history
- `alembic -c app/migrations/alembic.ini show <revision>` - Show details of a specific revision
- `alembic -c app/migrations/alembic.ini downgrade <revision>` - Downgrade to a specific revision