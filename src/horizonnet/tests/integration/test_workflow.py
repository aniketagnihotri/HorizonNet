"""Integration tests."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from horizonnet import (
    CreditEntityDataset,
    CreditEntityGraph,
    GAT,
    CreditAssessmentAgent
)


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete end-to-end workflow."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.dataset = CreditEntityDataset(num_entities=20, seed=42)
        self.data = self.dataset.generate_synthetic_data()
    
    def test_complete_pipeline(self):
        """Test complete pipeline."""
        # Build graph
        graph = CreditEntityGraph(self.data['features'], similarity_threshold=0.6)
        graph.build_knn_graph(k=3)
        adj_matrix = graph.get_adjacency_matrix()
        
        # Create model
        model = GAT(
            in_features=self.data['features'].shape[1],
            hidden_features=[16, 8],
            num_classes=3,
            num_heads=1
        )
        
        # Create agent
        agent = CreditAssessmentAgent(model, graph, self.dataset)
        
        # Perform assessment
        assessment = agent.assess_entity(0, self.data['features'], adj_matrix)
        
        self.assertIn('entity_index', assessment)
        self.assertIn('predicted_risk_level', assessment)
        self.assertIn('confidence', assessment)
        self.assertIn('recommendation', assessment)
    
    def test_batch_assessment(self):
        """Test batch assessment."""
        graph = CreditEntityGraph(self.data['features'], similarity_threshold=0.6)
        graph.build_knn_graph(k=3)
        adj_matrix = graph.get_adjacency_matrix()
        
        model = GAT(
            in_features=self.data['features'].shape[1],
            hidden_features=[16, 8],
            num_classes=3
        )
        
        agent = CreditAssessmentAgent(model, graph, self.dataset)
        
        # Batch assessment
        indices = [0, 5, 10]
        results = agent.assess_batch(indices, self.data['features'], adj_matrix)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['entity_index'], 0)


if __name__ == '__main__':
    unittest.main()
