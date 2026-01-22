"""
Credit Entity Graph Construction
Builds and manages the graph structure for credit entities using similarity metrics.
"""

import numpy as np
from typing import Tuple
from scipy.spatial.distance import cdist
from scipy.sparse import csr_matrix


class CreditEntityGraph:
    """Constructs and manages graphs of credit entities."""
    
    def __init__(self, features: np.ndarray, similarity_threshold: float = 0.5):
        """
        Initialize graph builder.
        
        Args:
            features: Node features (num_nodes, num_features)
            similarity_threshold: Threshold for creating edges
        """
        self.features = features
        self.num_nodes = features.shape[0]
        self.similarity_threshold = similarity_threshold
        self.adjacency_matrix = None
        self.edge_index = None
        self.edge_weights = None
        
    def build_graph(self, method: str = 'cosine') -> Tuple[np.ndarray, np.ndarray]:
        """
        Build graph from entity features using similarity.
        
        Args:
            method: Distance metric ('cosine', 'euclidean', 'correlation')
            
        Returns:
            Tuple of (edge_index, edge_weights)
        """
        if method == 'cosine':
            distances = cdist(self.features, self.features, metric='cosine')
            similarity = 1 - distances
        elif method == 'euclidean':
            distances = cdist(self.features, self.features, metric='euclidean')
            similarity = np.exp(-distances)
        elif method == 'correlation':
            similarity = np.corrcoef(self.features)
            similarity = np.abs(similarity)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        edges = []
        weights = []
        
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if similarity[i, j] > self.similarity_threshold:
                    edges.append([i, j])
                    edges.append([j, i])
                    weights.append(similarity[i, j])
                    weights.append(similarity[i, j])
        
        self.edge_index = np.array(edges).T if edges else np.array([[], []])
        self.edge_weights = np.array(weights)
        
        return self.edge_index, self.edge_weights
    
    def build_knn_graph(self, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Build k-nearest neighbors graph.
        
        Args:
            k: Number of nearest neighbors
            
        Returns:
            Tuple of (edge_index, edge_weights)
        """
        distances = cdist(self.features, self.features, metric='euclidean')
        
        edges = []
        weights = []
        
        for i in range(self.num_nodes):
            nearest_indices = np.argsort(distances[i])[:k+1][1:]
            
            for j in nearest_indices:
                edges.append([i, j])
                weight = np.exp(-distances[i, j])
                weights.append(weight)
        
        self.edge_index = np.array(edges).T if edges else np.array([[], []])
        self.edge_weights = np.array(weights)
        
        return self.edge_index, self.edge_weights
    
    def get_adjacency_matrix(self, weight_edges: bool = True) -> csr_matrix:
        """
        Get sparse adjacency matrix.
        
        Args:
            weight_edges: Whether to use edge weights
            
        Returns:
            Sparse adjacency matrix
        """
        if self.edge_index is None:
            raise RuntimeError("Graph not built. Call build_graph() first.")
        
        if self.edge_index.shape[1] == 0:
            self.adjacency_matrix = csr_matrix((self.num_nodes, self.num_nodes))
        else:
            if weight_edges and len(self.edge_weights) > 0:
                data = self.edge_weights
            else:
                data = np.ones(self.edge_index.shape[1])
            
            self.adjacency_matrix = csr_matrix(
                (data, (self.edge_index[0], self.edge_index[1])),
                shape=(self.num_nodes, self.num_nodes)
            )
        
        return self.adjacency_matrix
    
    def get_node_degrees(self) -> np.ndarray:
        """Get degree of each node."""
        adj_matrix = self.get_adjacency_matrix()
        return np.array(adj_matrix.sum(axis=1)).flatten()
    
    def get_graph_statistics(self) -> dict:
        """Get statistics about the graph."""
        if self.edge_index is None:
            return {'num_nodes': self.num_nodes, 'num_edges': 0, 'density': 0.0}
        
        num_edges = self.edge_index.shape[1]
        max_edges = self.num_nodes * (self.num_nodes - 1)
        density = num_edges / max_edges if max_edges > 0 else 0
        
        return {
            'num_nodes': self.num_nodes,
            'num_edges': num_edges,
            'density': density,
            'avg_degree': 2 * num_edges / self.num_nodes if self.num_nodes > 0 else 0
        }
    
    def visualize_adjacency(self) -> np.ndarray:
        """Return adjacency matrix for visualization."""
        return self.get_adjacency_matrix().toarray()
