.PHONY: help install test clean lint

help:
	@echo "Outlook AI Assistant - Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up generated files"
	@echo "  make lint       - Run Python syntax check"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

lint:
	python -m py_compile *.py
	@echo "✓ All Python files compile successfully"
