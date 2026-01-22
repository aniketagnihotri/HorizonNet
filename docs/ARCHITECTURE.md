# Architecture

## System Overview

HorizonNet follows a modular, layered architecture designed for production use and academic extensibility:

```
┌─────────────────────────────────────────┐
│     CreditAssessmentAgent               │
│  (Risk Assessment & Decisions)          │
└────────────────┬────────────────────────┘
                 │
     ┌───────────┴──────────────┐
     ▼                          ▼
┌─────────────────┐    ┌────────────────┐
│  GAT Model      │    │  Graph Module  │
│  (Neural Net)   │    │  (Relationships)
└────────┬────────┘    └────────┬───────┘
         │                      │
         └──────────┬───────────┘
                    ▼
            ┌──────────────────┐
            │ CreditEntity     │
            │ Dataset          │
            │ (Data Loading)   │
            └──────────────────┘
```

## Module Breakdown

### 1. Data Module (`data/`)
**Responsibility**: Data loading, preprocessing, and management

- **dataset.py**: `CreditEntityDataset` class
  - Synthetic data generation
  - CSV loading
  - Feature normalization
  - Train/test splitting

**Key Classes**:
- `CreditEntityDataset`: Manages all data operations

### 2. Graph Module (`graph/`)
**Responsibility**: Graph construction and manipulation

- **builder.py**: `CreditEntityGraph` class
  - Graph construction from features
  - Multiple similarity metrics
  - K-NN graph building
  - Adjacency matrix generation
  - Graph statistics

**Key Classes**:
- `CreditEntityGraph`: Builds and manages entity relationship graphs

### 3. Models Module (`models/`)
**Responsibility**: Neural network implementations

- **base.py**: Abstract base class for all models
- **gat.py**: Graph Attention Network implementation
  - `GraphAttentionLayer`: Single GAT layer with attention mechanism
  - `GAT`: Complete GAT model with multiple layers

**Key Classes**:
- `BaseModel`: Abstract base for extensibility
- `GraphAttentionLayer`: Attention computation
- `GAT`: Complete model

### 4. Agents Module (`agents/`)
**Responsibility**: Decision-making and assessment

- **assessment.py**: `CreditAssessmentAgent` class
  - Single entity assessment
  - Batch assessment
  - Risk classification
  - Report generation
  - Risk factor analysis

**Key Classes**:
- `RiskLevel`: Enum for risk categories
- `CreditAssessmentAgent`: Main decision agent

### 5. Utils Module (`utils/`)
**Responsibility**: Configuration and utilities

- **config.py**: Configuration management
- **logging.py**: Logging setup

**Key Classes**:
- `Config`: Centralized configuration
- `setup_logging()`: Logger initialization

## Data Flow

### Assessment Pipeline

```
Raw Features
    ↓
[Dataset Module] ← Normalization
    ↓
Features + Labels
    ↓
[Graph Module] ← Similarity Computation
    ↓
Graph (Adjacency Matrix)
    ↓
[GAT Model] ← Feature Aggregation via Attention
    ↓
Risk Probabilities
    ↓
[Assessment Agent] ← Decision Logic
    ↓
Risk Assessment + Recommendation + Report
```

## Design Patterns

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- Data handling
- Graph operations
- Model computation
- Business logic (assessment)

### 2. Modularity
Independent modules allow:
- Easy testing
- Clear dependencies
- Extensibility

### 3. Inheritance
`BaseModel` provides common interface for all models.

### 4. Configuration
`Config` class centralizes all hyperparameters.

## Extension Points

### Adding New Graph Builders
```python
class MyGraphBuilder(CreditEntityGraph):
    def build_custom_graph(self):
        # Custom graph building logic
        pass
```

### Adding New Models
```python
class MyModel(BaseModel):
    def forward(self, *args, **kwargs):
        # Custom model logic
        pass
    
    def predict(self, *args, **kwargs):
        # Custom prediction logic
        pass
```

### Adding New Assessment Logic
```python
class MyAgent(CreditAssessmentAgent):
    def custom_assessment(self, *args, **kwargs):
        # Custom assessment logic
        pass
```

## Dependencies

### Core Dependencies
- `numpy`: Numerical computing
- `pandas`: Data manipulation
- `scikit-learn`: Machine learning utilities
- `scipy`: Scientific computing (sparse matrices)

### Development Dependencies
- `pytest`: Testing
- `coverage`: Coverage reporting
- `black`: Code formatting
- `pylint`: Code linting

See `requirements.txt` and `requirements-dev.txt` for versions.
