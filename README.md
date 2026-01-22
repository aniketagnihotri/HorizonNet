# HorizonNet: Graph Attention Networks for Credit Risk Assessment

[![Tests](https://github.com/yourusername/HorizonNet/workflows/Tests/badge.svg)](https://github.com/yourusername/HorizonNet/actions/workflows/tests.yml)
[![Lint](https://github.com/yourusername/HorizonNet/workflows/Lint/badge.svg)](https://github.com/yourusername/HorizonNet/actions/workflows/lint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

**HorizonNet** is a production-grade Graph Attention Network (GAT) framework for transparent, interpretable credit entity risk assessment. Leveraging attention-based graph neural networks, HorizonNet enables financial institutions to make explainable credit decisions with confidence scores and detailed risk factor analysis.

### Key Capabilities

- 🧠 **Graph Attention Networks**: State-of-the-art attention mechanism for learning entity relationships
- 📊 **Interpretable Decisions**: Explainable risk predictions with confidence scores
- 🎯 **Risk Factor Analysis**: Identification of key features driving risk assessments
- ⚡ **Batch Processing**: Efficient assessment of multiple entities
- 🔧 **Production Ready**: Comprehensive error handling, logging, and testing
- 📈 **Extensible Architecture**: Clean modular separation

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/HorizonNet.git
cd HorizonNet
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Basic Usage

```python
from horizonnet import CreditEntityDataset, CreditEntityGraph, GAT, CreditAssessmentAgent

dataset = CreditEntityDataset(num_entities=100)
data = dataset.generate_synthetic_data()

graph = CreditEntityGraph(data['features'])
graph.build_knn_graph(k=5)
adj_matrix = graph.get_adjacency_matrix()

model = GAT(
    in_features=data['features'].shape[1],
    hidden_features=[16, 8],
    num_classes=3
)

agent = CreditAssessmentAgent(model, graph, dataset)
assessment = agent.assess_entity(0, data['features'], adj_matrix)
print(agent.generate_report(assessment))
```

## Project Structure

```
HorizonNet/
├── src/horizonnet/              # Main package
│   ├── models/                  # GAT neural network
│   ├── graph/                   # Graph construction
│   ├── data/                    # Dataset handling
│   ├── agents/                  # Assessment agents
│   └── utils/                   # Configuration
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── examples/                    # Example scripts
├── docs/                        # Documentation
├── .github/                     # GitHub workflows (CI/CD)
├── docker/                      # Docker setup
├── setup.py                     # Package setup
├── pyproject.toml              # Package config
└── Makefile                    # Development tasks
```

## Development

```bash
make test         # Run tests
make lint         # Linting
make format       # Format code
make check        # All checks
make example      # Run demo
```

## Documentation

- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Development](docs/DEVELOPMENT.md)
- [Contributing](.github/CONTRIBUTING.md)

## License

MIT License - see LICENSE file

## Citation

```bibtex
@software{horizonnet2024,
  title={HorizonNet: Graph Attention Networks for Credit Risk Assessment},
  author={Development Team},
  year={2024},
  url={https://github.com/yourusername/HorizonNet}
}
```

---

**Built with ❤️ for transparent AI in finance**