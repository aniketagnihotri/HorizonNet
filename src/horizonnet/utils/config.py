"""Configuration management."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Application configuration."""
    
    # Model settings
    input_features: int = 8
    hidden_features: list = None
    num_classes: int = 3
    num_heads: int = 1
    dropout: float = 0.1
    learning_rate: float = 0.01
    
    # Graph settings
    similarity_threshold: float = 0.6
    k_nearest_neighbors: int = 5
    graph_method: str = 'knn'  # 'similarity' or 'knn'
    
    # Dataset settings
    num_entities: int = 100
    train_test_split: float = 0.8
    random_seed: int = 42
    
    # Logging
    log_level: str = 'INFO'
    log_file: Optional[str] = None
    
    def __post_init__(self):
        """Set defaults after initialization."""
        if self.hidden_features is None:
            self.hidden_features = [16, 8]
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'Config':
        """Create config from dictionary."""
        return cls(**config_dict)
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            'input_features': self.input_features,
            'hidden_features': self.hidden_features,
            'num_classes': self.num_classes,
            'num_heads': self.num_heads,
            'dropout': self.dropout,
            'learning_rate': self.learning_rate,
            'similarity_threshold': self.similarity_threshold,
            'k_nearest_neighbors': self.k_nearest_neighbors,
            'graph_method': self.graph_method,
            'num_entities': self.num_entities,
            'train_test_split': self.train_test_split,
            'random_seed': self.random_seed,
            'log_level': self.log_level,
            'log_file': self.log_file,
        }
