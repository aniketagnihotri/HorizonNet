"""
Graph Attention Network (GAT) Model
Implements GAT for credit entity risk assessment.
"""

import numpy as np
from typing import Optional
import warnings

from .base import BaseModel

warnings.filterwarnings('ignore')


class GraphAttentionLayer:
    """Single Graph Attention Layer."""
    
    def __init__(self, in_features: int, out_features: int, num_heads: int = 1, 
                 dropout: float = 0.0, activation: Optional[str] = 'relu'):
        """
        Initialize GAT layer.
        
        Args:
            in_features: Input feature dimension
            out_features: Output feature dimension
            num_heads: Number of attention heads
            dropout: Dropout rate
            activation: Activation function ('relu', 'sigmoid', or None)
        """
        self.in_features = in_features
        self.out_features = out_features
        self.num_heads = num_heads
        self.dropout = dropout
        self.activation = activation
        
        # Initialize weights
        self.W = np.random.randn(in_features, out_features) * np.sqrt(2.0 / in_features)
        self.a = np.random.randn(2 * out_features, 1) * np.sqrt(2.0 / (2 * out_features))
        self.bias = np.zeros((1, out_features))
        
    def apply_activation(self, x: np.ndarray) -> np.ndarray:
        """Apply activation function."""
        if self.activation == 'relu':
            return np.maximum(0, x)
        elif self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        return x
    
    def softmax(self, x: np.ndarray, axis: int = 1) -> np.ndarray:
        """Numerically stable softmax."""
        x_shifted = x - np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(np.clip(x_shifted, -500, 500))
        return exp_x / (np.sum(exp_x, axis=axis, keepdims=True) + 1e-8)
    
    def forward(self, features: np.ndarray, adj_matrix: np.ndarray) -> np.ndarray:
        """
        Forward pass through GAT layer.
        
        Args:
            features: Node features (num_nodes, in_features)
            adj_matrix: Adjacency matrix (num_nodes, num_nodes)
            
        Returns:
            Output features (num_nodes, out_features)
        """
        num_nodes = features.shape[0]
        
        # Linear transformation
        h = np.dot(features, self.W) + self.bias
        
        # Compute attention coefficients
        a_input = np.concatenate([
            np.repeat(h, num_nodes, axis=0),
            np.tile(h, (num_nodes, 1))
        ], axis=1)
        
        e = np.dot(a_input, self.a).reshape((num_nodes, num_nodes))
        e = self.apply_activation(e)
        
        # Mask attention by adjacency matrix
        adj_dense = adj_matrix.toarray() if hasattr(adj_matrix, 'toarray') else adj_matrix
        adj_mask = adj_dense + np.eye(num_nodes)
        
        e = np.where(adj_mask > 0, e, -1e9)
        attention_weights = self.softmax(e, axis=1)
        
        # Apply dropout
        if self.dropout > 0:
            mask = np.random.binomial(1, 1 - self.dropout, attention_weights.shape)
            attention_weights = attention_weights * mask / (1 - self.dropout + 1e-8)
        
        # Aggregate features
        output = np.dot(attention_weights, h)
        
        return output


class GAT(BaseModel):
    """Graph Attention Network for credit entity risk assessment."""
    
    def __init__(self, in_features: int, hidden_features: list, num_classes: int,
                 num_heads: int = 1, dropout: float = 0.0, learning_rate: float = 0.01):
        """
        Initialize GAT model.
        
        Args:
            in_features: Input feature dimension
            hidden_features: List of hidden layer dimensions
            num_classes: Number of output classes
            num_heads: Number of attention heads
            dropout: Dropout rate
            learning_rate: Learning rate for optimization
        """
        super().__init__()
        self.in_features = in_features
        self.hidden_features = hidden_features
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        
        # Build layers
        self.layers = []
        prev_dim = in_features
        
        for hidden_dim in hidden_features:
            self.layers.append(
                GraphAttentionLayer(prev_dim, hidden_dim, num_heads, dropout, 'relu')
            )
            prev_dim = hidden_dim
        
        # Output layer
        self.layers.append(
            GraphAttentionLayer(prev_dim, num_classes, num_heads, dropout, 'sigmoid')
        )
        
        self.training_history = []
    
    def forward(self, features: np.ndarray, adj_matrix: np.ndarray) -> np.ndarray:
        """
        Forward pass through GAT.
        
        Args:
            features: Node features
            adj_matrix: Adjacency matrix
            
        Returns:
            Output predictions
        """
        x = features.copy()
        
        for layer in self.layers[:-1]:
            x = layer.forward(x, adj_matrix)
        
        output = self.layers[-1].forward(x, adj_matrix)
        
        return output
    
    def predict(self, features: np.ndarray, adj_matrix: np.ndarray) -> np.ndarray:
        """
        Get predictions.
        
        Args:
            features: Node features
            adj_matrix: Adjacency matrix
            
        Returns:
            Predicted class labels
        """
        output = self.forward(features, adj_matrix)
        return np.argmax(output, axis=1)
    
    def predict_proba(self, features: np.ndarray, adj_matrix: np.ndarray) -> np.ndarray:
        """
        Get prediction probabilities.
        
        Args:
            features: Node features
            adj_matrix: Adjacency matrix
            
        Returns:
            Probability for each class
        """
        output = self.forward(features, adj_matrix)
        exp_output = np.exp(output - np.max(output, axis=1, keepdims=True))
        return exp_output / np.sum(exp_output, axis=1, keepdims=True)
    
    def summary(self) -> str:
        """Return model summary."""
        summary = "Graph Attention Network (GAT) Model\n"
        summary += f"Input features: {self.in_features}\n"
        summary += f"Hidden layers: {self.hidden_features}\n"
        summary += f"Output classes: {self.num_classes}\n"
        summary += f"Total layers: {len(self.layers)}\n"
        return summary
