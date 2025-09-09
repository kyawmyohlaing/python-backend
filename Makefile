COMPOSE_DEV=docker-compose -f docker-compose.yml -f docker-compose.override.yml
COMPOSE_PROD=docker-compose -f docker-compose.yml

.PHONY: help dev prod down logs migrate test clean setup backup

help:
	@echo "FastAPI Backend Template - Makefile Commands"
	@echo "=========================================="
	@echo "  make dev       - Start development environment (hot reload)"
	@echo "  make prod      - Start production environment (Gunicorn)"
	@echo "  make down      - Stop all containers"
	@echo "  make logs      - View application logs"
	@echo "  make migrate   - Run database migrations"
	@echo "  make test      - Run test suite"
	@echo "  make clean     - Remove Docker containers, networks, and volumes"
	@echo "  make setup     - Setup environment (copy .env.example to .env)"
	@echo "  make backup    - Create a database backup"

dev:
	@echo "Starting development environment..."
	$(COMPOSE_DEV) up --build

prod:
	@echo "Starting production environment..."
	$(COMPOSE_PROD) up --build -d

down:
	@echo "Stopping all containers..."
	docker-compose down

logs:
	@echo "Viewing application logs..."
	docker-compose logs -f web

migrate:
	@echo "Running database migrations..."
	docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head

test:
	@echo "Running test suite..."
	python -m pytest tests/ -v

clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans

setup:
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example"; \
		echo "Please review and update the .env file with your configuration"; \
	else \
		echo ".env file already exists"; \
	fi

backup:
	@echo "Creating database backup..."
	@if [ -f "backup_once.sh" ]; then \
		chmod +x backup_once.sh && ./backup_once.sh; \
	elif [ -f "backup_once.bat" ]; then \
		./backup_once.bat; \
	else \
		echo "Backup script not found. Please ensure backup_once.sh or backup_once.bat exists."; \
		exit 1; \
	fi
