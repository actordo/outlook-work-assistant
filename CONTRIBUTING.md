# Contributing to Outlook Assistant

Thank you for your interest in contributing to the Outlook AI Assistant! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/outlook-assistant.git
   cd outlook-assistant
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with test credentials

## Running Tests

Run the test suite with pytest:

```bash
pytest tests/ -v
```

For test coverage report:

```bash
pytest tests/ --cov=. --cov-report=html
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

## Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Commit your changes with a clear message
6. Push to your fork
7. Open a pull request

## Pull Request Guidelines

- Describe what your PR does
- Reference any related issues
- Ensure tests pass
- Update documentation if needed
- Keep changes focused and minimal

## Reporting Issues

When reporting issues, please include:

- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (Python version, OS, etc.)

## Security

If you discover a security vulnerability, please email the maintainers directly rather than opening a public issue.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
