"""
HorizonNet: Graph Attention Network for Credit Entity Risk Assessment

A production-grade framework for credit risk assessment using Graph Attention Networks.
Enables transparent, interpretable credit decisions through attention-based graph analytics.
"""

__version__ = "1.0.0"
__author__ = "Development Team"
__license__ = "MIT"

from .models.gat import GAT
from .graph.builder import CreditEntityGraph
from .data.dataset import CreditEntityDataset
from .agents.assessment import CreditAssessmentAgent

__all__ = [
    "GAT",
    "CreditEntityGraph",
    "CreditEntityDataset",
    "CreditAssessmentAgent",
]
