# Contributing to HorizonNet

Thank you for your interest in contributing! This document provides guidelines for contributing.

## Code of Conduct

Be respectful, inclusive, and professional.

## How to Contribute

### Reporting Bugs

Create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### Suggesting Features

Create an issue with:
- Feature description
- Use case and benefits
- Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes following code style guidelines
4. Add/update tests
5. Update documentation as needed
6. Push to your fork
7. Create a pull request with clear description

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints where applicable
- Maximum line length: 100 characters
- Docstrings in NumPy style

### Testing Requirements
- All new code must have tests
- Maintain >80% code coverage
- Tests must pass: `make test`

### Commit Messages
- Use clear, descriptive messages
- Reference issues when relevant: "Fixes #123"
- Use conventional commits when possible

## Running Locally

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run all checks
make check
```

## Questions?

Open an issue or contact the maintainers.
