"""Base classes for neural network models."""

from abc import ABC, abstractmethod
import numpy as np


class BaseModel(ABC):
    """Abstract base class for all models."""
    
    def __init__(self):
        """Initialize base model."""
        self.is_trained = False
    
    @abstractmethod
    def forward(self, *args, **kwargs) -> np.ndarray:
        """Forward pass through model."""
        pass
    
    @abstractmethod
    def predict(self, *args, **kwargs) -> np.ndarray:
        """Make predictions."""
        pass
    
    def summary(self) -> str:
        """Return model summary."""
        raise NotImplementedError
