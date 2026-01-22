.PHONY: help install test test-unit test-integration test-coverage lint format check clean

help:
	@echo "HorizonNet Development Commands"
	@echo "==============================="
	@echo "  make install          Install dependencies"
	@echo "  make test             Run all tests"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-coverage    Run tests with coverage report"
	@echo "  make lint             Run linting checks"
	@echo "  make format           Format code with black"
	@echo "  make check            Run all checks (lint + format)"
	@echo "  make clean            Clean build artifacts"
	@echo "  make example          Run example"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-coverage:
	pytest tests/ --cov=src/horizonnet --cov-report=html --cov-report=term

lint:
	black --check src/ tests/ examples/
	pylint src/ tests/ || true
	flake8 src/ tests/ --max-line-length=100 || true

format:
	black src/ tests/ examples/

check: lint format

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete || true
	rm -rf .pytest_cache .coverage htmlcov *.egg-info dist build || true

example:
	python examples/credit_assessment_demo.py
