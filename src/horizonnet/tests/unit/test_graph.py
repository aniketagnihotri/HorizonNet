"""Unit tests for graph module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from horizonnet.graph.builder import CreditEntityGraph


class TestCreditEntityGraph(unittest.TestCase):
    """Test CreditEntityGraph."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.features = np.random.randn(10, 8)
        self.graph = CreditEntityGraph(self.features, similarity_threshold=0.5)
    
    def test_build_graph_cosine(self):
        """Test graph building with cosine similarity."""
        edge_index, edge_weights = self.graph.build_graph(method='cosine')
        
        self.assertIsNotNone(edge_index)
        self.assertIsNotNone(edge_weights)
    
    def test_build_knn_graph(self):
        """Test k-NN graph building."""
        edge_index, edge_weights = self.graph.build_knn_graph(k=3)
        
        self.assertIsNotNone(edge_index)
        self.assertEqual(len(edge_weights), edge_index.shape[1])
    
    def test_adjacency_matrix(self):
        """Test adjacency matrix generation."""
        self.graph.build_knn_graph(k=3)
        adj_matrix = self.graph.get_adjacency_matrix()
        
        self.assertEqual(adj_matrix.shape, (10, 10))
    
    def test_graph_statistics(self):
        """Test graph statistics computation."""
        self.graph.build_knn_graph(k=3)
        stats = self.graph.get_graph_statistics()
        
        self.assertIn('num_nodes', stats)
        self.assertIn('num_edges', stats)
        self.assertIn('density', stats)
        self.assertIn('avg_degree', stats)
        self.assertEqual(stats['num_nodes'], 10)


if __name__ == '__main__':
    unittest.main()
