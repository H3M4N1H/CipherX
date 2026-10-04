.PHONY: help install dev test lint fmt type check clean build

help:
	@echo "install  Install the package"
	@echo "dev      Install with dev + full extras (editable)"
	@echo "test     Run the test suite with coverage"
	@echo "lint     Run ruff"
	@echo "fmt      Format with black + ruff --fix"
	@echo "type     Run mypy"
	@echo "check    Run lint + type + test (what CI runs)"
	@echo "build    Build sdist and wheel"
	@echo "clean    Remove build/test artifacts"

install:
	pip install .

dev:
	pip install -e ".[dev,full]"
	pre-commit install

test:
	pytest --cov --cov-report=term-missing

lint:
	ruff check cipherx tests

fmt:
	black cipherx tests
	ruff check --fix cipherx tests

type:
	mypy cipherx

check: lint type test
	black --check cipherx tests

build:
	python -m build

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
