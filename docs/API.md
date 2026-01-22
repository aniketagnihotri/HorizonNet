# API Reference

## Core Classes

### CreditEntityDataset

Dataset management and preprocessing.

```python
from horizonnet import CreditEntityDataset

dataset = CreditEntityDataset(num_entities=100, seed=42)
data = dataset.generate_synthetic_data()
train_data, test_data = dataset.split_train_test(data, train_ratio=0.8)
```

**Methods:**
- `generate_synthetic_data()` - Generate synthetic credit entity data
- `load_from_csv(filepath)` - Load data from CSV file
- `split_train_test(data, train_ratio)` - Split into train/test sets
- `get_feature_names()` - Get credit feature names

### CreditEntityGraph

Graph construction from entity features.

```python
from horizonnet import CreditEntityGraph

graph = CreditEntityGraph(features, similarity_threshold=0.6)
edge_index, weights = graph.build_knn_graph(k=5)
adj_matrix = graph.get_adjacency_matrix()
stats = graph.get_graph_statistics()
```

**Methods:**
- `build_graph(method)` - Build similarity-based graph
- `build_knn_graph(k)` - Build k-nearest neighbors graph
- `get_adjacency_matrix(weight_edges)` - Get sparse adjacency matrix
- `get_node_degrees()` - Get node degree values
- `get_graph_statistics()` - Get graph metrics

### GAT

Graph Attention Network model.

```python
from horizonnet import GAT

model = GAT(
    in_features=8,
    hidden_features=[16, 8],
    num_classes=3,
    num_heads=1,
    dropout=0.1
)

predictions = model.predict(features, adj_matrix)
probabilities = model.predict_proba(features, adj_matrix)
print(model.summary())
```

**Methods:**
- `forward(features, adj_matrix)` - Forward pass
- `predict(features, adj_matrix)` - Get predictions
- `predict_proba(features, adj_matrix)` - Get probabilities
- `summary()` - Model summary

### CreditAssessmentAgent

Credit risk assessment agent.

```python
from horizonnet import CreditAssessmentAgent

agent = CreditAssessmentAgent(model, graph, dataset)
assessment = agent.assess_entity(entity_idx, features, adj_matrix)
report = agent.generate_report(assessment)
```

**Methods:**
- `assess_entity(entity_idx, features, adj_matrix)` - Assess single entity
- `assess_batch(indices, features, adj_matrix)` - Assess multiple entities
- `generate_report(assessment)` - Generate text report
- `get_assessment_summary()` - Get summary statistics

## Risk Levels

```python
from horizonnet.agents import RiskLevel

# Risk classification
RiskLevel.LOW      # 0 - Low credit risk
RiskLevel.MEDIUM   # 1 - Medium credit risk
RiskLevel.HIGH     # 2 - High credit risk
```

## Configuration

```python
from horizonnet.utils import Config

config = Config(
    input_features=8,
    hidden_features=[16, 8],
    num_classes=3,
    num_heads=1,
    dropout=0.1,
    learning_rate=0.01,
    similarity_threshold=0.6,
    k_nearest_neighbors=5,
    num_entities=100,
    random_seed=42
)

# Convert to/from dict
config_dict = config.to_dict()
new_config = Config.from_dict(config_dict)
```

## Utilities

### Logging

```python
from horizonnet.utils import setup_logging

logger = setup_logging(
    name='horizonnet',
    level='INFO',
    log_file='app.log'
)
```
