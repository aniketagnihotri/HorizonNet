# HorizonNet Documentation

## Overview

HorizonNet is a production-grade Graph Attention Network (GAT) framework for transparent, interpretable credit entity risk assessment. Leveraging attention-based graph analytics, HorizonNet provides explainable credit decisions with confidence scores and risk factor analysis.

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## Quick Start

```python
from horizonnet import CreditEntityDataset, CreditEntityGraph, GAT, CreditAssessmentAgent

# Load data
dataset = CreditEntityDataset(num_entities=100)
data = dataset.generate_synthetic_data()

# Build graph
graph = CreditEntityGraph(data['features'])
graph.build_knn_graph(k=5)
adj_matrix = graph.get_adjacency_matrix()

# Initialize model
model = GAT(
    in_features=data['features'].shape[1],
    hidden_features=[16, 8],
    num_classes=3
)

# Create agent and assess
agent = CreditAssessmentAgent(model, graph, dataset)
assessment = agent.assess_entity(0, data['features'], adj_matrix)
report = agent.generate_report(assessment)
print(report)
```

## Architecture

HorizonNet follows a modular, production-ready architecture:

```
src/horizonnet/
├── models/          # Neural network models (GAT)
├── graph/           # Graph construction utilities
├── data/            # Dataset handling
├── agents/          # Credit assessment agents
└── utils/           # Configuration and logging
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed information.

## Features

- **Graph Attention Networks**: Attention-based graph neural networks for entity relationships
- **Interpretable Decisions**: Explainable risk predictions with confidence scores
- **Risk Factor Analysis**: Identification of key factors driving risk assessments
- **Batch Processing**: Efficient assessment of multiple entities
- **Flexible Graph Construction**: Multiple graph building strategies (k-NN, similarity-based)
- **Production Ready**: Comprehensive error handling, logging, and testing

## Installation

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

## Usage

See [examples/credit_assessment_demo.py](../examples/credit_assessment_demo.py) for a complete working example.

### Running Tests

```bash
make test           # Run all tests
make test-unit      # Run unit tests only
make test-coverage  # Run tests with coverage report
```

## API Reference

See [API.md](API.md) for comprehensive API documentation.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](../github/CONTRIBUTING.md) for guidelines.
