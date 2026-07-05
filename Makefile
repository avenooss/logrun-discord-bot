.PHONY: help install install-dev run format lint type-check test test-cov clean docker-build docker-up docker-down migrate

.DEFAULT_GOAL := help

help:  ## Display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

run:  ## Run the bot
	python -m src.main

format:  ## Format code with Black and isort
	black src tests
	isort src tests

lint:  ## Run flake8 linting
	flake8 src tests

type-check:  ## Run mypy type checking
	mypy src

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=src --cov-report=html --cov-report=term

test-watch:  ## Run tests in watch mode
	pytest-watch

clean:  ## Clean up cache and build files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info

docker-build:  ## Build Docker image
	docker build -t logrun-bot:latest .

docker-up:  ## Start Docker containers
	docker-compose up -d

docker-down:  ## Stop Docker containers
	docker-compose down

docker-logs:  ## View Docker logs
	docker-compose logs -f bot

db-init:  ## Initialize database
	python -m alembic upgrade head

db-migrate:  ## Create new database migration
	python -m alembic revision --autogenerate -m "$(m)"
