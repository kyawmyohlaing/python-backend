# Makefile for FastAPI backend template

# Variables
PYTHON = python3
PYTEST = pytest
APP_DIR = app
TESTS_DIR = tests

# Default target
.PHONY: help
help:
	@echo "FastAPI Backend Template - Available Commands:"
	@echo "  make dev          - Start development server"
	@echo "  make prod         - Start production server"
	@echo "  make test         - Run all tests"
	@echo "  make test-tables  - Run table management tests"
	@echo "  make test-users   - Run user-related tests"
	@echo "  make migrate      - Run database migrations"
	@echo "  make clean        - Clean Python cache files"
	@echo "  make logs         - View container logs"
	@echo "  make backup       - Create database backup"
	@echo "  make restore      - Restore database from backup"

# Development server
.PHONY: dev
dev:
	docker-compose up -d

# Production server
.PHONY: prod
prod:
	docker-compose -f docker-compose.yml up -d

# Run all tests
.PHONY: test
test:
	$(PYTHON) -m $(PYTEST) $(TESTS_DIR) -v

# Run table management tests
.PHONY: test-tables
test-tables:
	$(PYTHON) run_table_tests.py

# Run user-related tests
.PHONY: test-users
test-users:
	$(PYTHON) -m $(PYTEST) $(TESTS_DIR)/test_users* -v

# Run database migrations
.PHONY: migrate
migrate:
	docker-compose run --rm web alembic upgrade head

# Clean Python cache files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	find . -type f -name ".DS_Store" -delete

# View container logs
.PHONY: logs
logs:
	docker-compose logs -f

# Create database backup
.PHONY: backup
backup:
	./backup_once.sh

# Restore database from backup
.PHONY: restore
restore:
	@echo "To restore database, use:"
	@echo "./restore_db.sh <backup_file>"