# Development Guide

## Setup

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/HorizonNet.git
cd HorizonNet

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Development Workflow

### Code Style

We follow PEP 8 guidelines with some extensions:

```bash
# Format code
black src/ tests/ examples/

# Lint code
pylint src/ tests/

# Check types (if available)
mypy src/
```

### Testing

```bash
# Run all tests
make test

# Run specific test file
python -m pytest tests/unit/test_models.py

# Run with coverage
coverage run -m pytest
coverage report
coverage html
```

### Pre-commit Checks

```bash
# Run all checks
make check
```

## Project Structure

```
HorizonNet/
├── src/horizonnet/          # Main package
│   ├── models/              # Model implementations
│   ├── graph/               # Graph utilities
│   ├── data/                # Data handling
│   ├── agents/              # Assessment agents
│   └── utils/               # Utilities
├── tests/                   # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── fixtures/            # Test data
├── examples/                # Example scripts
├── docs/                    # Documentation
├── config/                  # Configuration files
└── docker/                  # Docker setup
```

## Common Tasks

### Running Examples

```bash
# Run credit assessment demo
python examples/credit_assessment_demo.py
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/my-feature`
2. Implement changes with tests
3. Run tests and linting: `make check`
4. Commit and push
5. Create pull request

### Debugging

```python
# Enable verbose logging
from horizonnet.utils import setup_logging
logger = setup_logging(level='DEBUG')

# Inspect model layers
print(model.summary())
```

## Performance Optimization

- Use sparse matrices for large graphs
- Batch process large datasets
- Consider using GPU acceleration for future versions

## Documentation

- Docstrings follow NumPy style
- Update API.md when adding new public classes
- Update ARCHITECTURE.md for structural changes

## Contributing

See [CONTRIBUTING.md](../.github/CONTRIBUTING.md)
