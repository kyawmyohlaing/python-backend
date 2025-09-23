# Makefile for FastAPI Backend

# Variables
PYTHON := python3
APP := app/main.py
TEST := tests/
REQ := requirements.txt

# Default target
.PHONY: help
help:
	@echo "FastAPI Backend Makefile"
	@echo "========================"
	@echo "dev     - Run development server"
	@echo "prod    - Run production server"
	@echo "test    - Run all tests"
	@echo "test-invoice - Run invoice functionality tests"
	@echo "install - Install dependencies"
	@echo "migrate - Run database migrations"
	@echo "logs    - Show server logs"
	@echo "clean   - Clean temporary files"

# Development server
.PHONY: dev
dev:
	PORT=8088 $(PYTHON) $(APP)

# Production server
.PHONY: prod
prod:
	gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8088

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest $(TEST) -v

# Run invoice tests
.PHONY: test-invoice
test-invoice:
	$(PYTHON) test_invoice_functionality.py

# Install dependencies
.PHONY: install
install:
	pip install -r $(REQ)

# Run migrations
.PHONY: migrate
migrate:
	alembic upgrade head

# Show logs
.PHONY: logs
logs:
	tail -f logs/app.log

# Clean temporary files
.PHONY: clean
clean:
	rm -rf __pycache__/
	rm -rf app/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf app/migrations/__pycache__/
	rm -rf logs/
	find . -type f -name "*.pyc" -delete