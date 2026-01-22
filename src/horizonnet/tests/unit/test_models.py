"""Unit tests for models."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from horizonnet.models.gat import GAT, GraphAttentionLayer


class TestGraphAttentionLayer(unittest.TestCase):
    """Test GraphAttentionLayer."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.layer = GraphAttentionLayer(8, 16, num_heads=1, dropout=0.0)
        self.features = np.random.randn(10, 8)
        self.adj_matrix = np.eye(10)
    
    def test_forward_pass(self):
        """Test forward pass through layer."""
        output = self.layer.forward(self.features, self.adj_matrix)
        
        self.assertEqual(output.shape, (10, 16))
        self.assertFalse(np.isnan(output).any())
    
    def test_activation_relu(self):
        """Test ReLU activation."""
        layer = GraphAttentionLayer(8, 16, activation='relu')
        x = np.array([[-1, 0, 1], [2, -3, 4]])
        output = layer.apply_activation(x)
        
        np.testing.assert_array_equal(output, np.array([[0, 0, 1], [2, 0, 4]]))
    
    def test_softmax_numerical_stability(self):
        """Test numerically stable softmax."""
        layer = GraphAttentionLayer(8, 16)
        x = np.array([[1000, 1001, 999], [-1000, -999, -1001]])
        output = layer.softmax(x, axis=1)
        
        # Check sum to 1
        np.testing.assert_array_almost_equal(output.sum(axis=1), np.ones(2))
        # Check all positive
        self.assertTrue((output > 0).all())


class TestGATModel(unittest.TestCase):
    """Test GAT model."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.model = GAT(
            in_features=8,
            hidden_features=[16, 8],
            num_classes=3,
            num_heads=1,
            dropout=0.0
        )
        self.features = np.random.randn(10, 8)
        self.adj_matrix = np.eye(10)
    
    def test_forward_pass(self):
        """Test model forward pass."""
        output = self.model.forward(self.features, self.adj_matrix)
        
        self.assertEqual(output.shape, (10, 3))
        self.assertFalse(np.isnan(output).any())
    
    def test_predict(self):
        """Test prediction."""
        predictions = self.model.predict(self.features, self.adj_matrix)
        
        self.assertEqual(predictions.shape, (10,))
        self.assertTrue(np.all(predictions >= 0) and np.all(predictions < 3))
    
    def test_predict_proba(self):
        """Test probability predictions."""
        probas = self.model.predict_proba(self.features, self.adj_matrix)
        
        self.assertEqual(probas.shape, (10, 3))
        # Check sums to 1
        np.testing.assert_array_almost_equal(probas.sum(axis=1), np.ones(10))
        # Check in [0, 1]
        self.assertTrue((probas >= 0).all() and (probas <= 1).all())


if __name__ == '__main__':
    unittest.main()
