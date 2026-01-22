"""
Credit Entity Assessment Agent
Agent for making credit risk decisions using the GAT model.
"""

import numpy as np
from typing import Dict, List, Optional
from enum import Enum


class RiskLevel(Enum):
    """Credit risk classification levels."""
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class CreditAssessmentAgent:
    """Agent for assessing credit risk of entities using GAT model."""
    
    def __init__(self, model, graph, dataset, risk_thresholds: Optional[Dict] = None):
        """
        Initialize credit assessment agent.
        
        Args:
            model: Trained GAT model
            graph: CreditEntityGraph instance
            dataset: CreditEntityDataset instance
            risk_thresholds: Dict with confidence thresholds for each risk level
        """
        self.model = model
        self.graph = graph
        self.dataset = dataset
        
        if risk_thresholds is None:
            self.risk_thresholds = {
                'low_to_medium': 0.4,
                'medium_to_high': 0.7
            }
        else:
            self.risk_thresholds = risk_thresholds
        
        self.assessment_history = []
    
    def assess_entity(self, entity_idx: int, features: np.ndarray,
                     adj_matrix) -> Dict:
        """
        Assess credit risk for a single entity.
        
        Args:
            entity_idx: Index of entity to assess
            features: All node features
            adj_matrix: Graph adjacency matrix
            
        Returns:
            Dictionary with assessment results
        """
        probabilities = self.model.predict_proba(features, adj_matrix)
        entity_probs = probabilities[entity_idx]
        predicted_class = np.argmax(entity_probs)
        confidence = np.max(entity_probs)
        
        risk_level = self._classify_risk(entity_probs)
        
        neighbors = self._get_neighbors(entity_idx, adj_matrix)
        neighbor_risks = [RiskLevel(np.argmax(probabilities[n])).name 
                         for n in neighbors[:5]]
        
        assessment = {
            'entity_index': entity_idx,
            'entity_name': self.dataset.generate_synthetic_data()['entity_names'][entity_idx],
            'predicted_risk_level': risk_level.name,
            'risk_probability': entity_probs,
            'confidence': confidence,
            'neighbors': neighbors[:5],
            'neighbor_risks': neighbor_risks,
            'recommendation': self._generate_recommendation(risk_level, confidence),
            'factors': self._analyze_risk_factors(entity_idx, features, entity_probs)
        }
        
        self.assessment_history.append(assessment)
        return assessment
    
    def assess_batch(self, indices: List[int], features: np.ndarray,
                    adj_matrix) -> List[Dict]:
        """
        Assess multiple entities.
        
        Args:
            indices: List of entity indices to assess
            features: All node features
            adj_matrix: Graph adjacency matrix
            
        Returns:
            List of assessment dictionaries
        """
        results = []
        for idx in indices:
            result = self.assess_entity(idx, features, adj_matrix)
            results.append(result)
        return results
    
    def _classify_risk(self, probabilities: np.ndarray) -> RiskLevel:
        """Classify risk level from probabilities."""
        predicted_class = np.argmax(probabilities)
        return RiskLevel(predicted_class)
    
    def _get_neighbors(self, entity_idx: int, adj_matrix) -> List[int]:
        """Get connected neighbors of an entity."""
        adj_array = adj_matrix.toarray() if hasattr(adj_matrix, 'toarray') else adj_matrix
        neighbors = np.where(adj_array[entity_idx] > 0)[0].tolist()
        neighbors = [n for n in neighbors if n != entity_idx]
        return neighbors
    
    def _generate_recommendation(self, risk_level: RiskLevel, 
                                confidence: float) -> str:
        """Generate recommendation based on risk assessment."""
        recommendations = {
            RiskLevel.LOW: {
                'action': 'APPROVE',
                'message': 'Low credit risk - recommend approval with standard terms'
            },
            RiskLevel.MEDIUM: {
                'action': 'REVIEW',
                'message': 'Medium credit risk - recommend detailed review with possible enhanced terms'
            },
            RiskLevel.HIGH: {
                'action': 'DECLINE',
                'message': 'High credit risk - recommend decline or only with substantial safeguards'
            }
        }
        
        rec = recommendations[risk_level]['message']
        
        if confidence < 0.6:
            rec += " (LOW CONFIDENCE - Further analysis recommended)"
        
        return rec
    
    def _analyze_risk_factors(self, entity_idx: int, features: np.ndarray,
                             probabilities: np.ndarray) -> Dict:
        """Analyze key risk factors for an entity."""
        feature_names = self.dataset.get_feature_names()
        entity_features = features[entity_idx]
        
        feature_importance = np.abs(entity_features) * probabilities[2]
        
        top_features = np.argsort(feature_importance)[-3:][::-1]
        
        factors = {}
        for feat_idx in top_features:
            factors[feature_names[feat_idx]] = {
                'value': float(entity_features[feat_idx]),
                'importance_score': float(feature_importance[feat_idx])
            }
        
        return factors
    
    def generate_report(self, assessment: Dict) -> str:
        """Generate human-readable report for assessment."""
        report = f"""
╔═══════════════════════════════════════════════════════════╗
║           CREDIT RISK ASSESSMENT REPORT                   ║
╚═══════════════════════════════════════════════════════════╝

Entity: {assessment['entity_name']} (ID: {assessment['entity_index']})
Risk Level: {assessment['predicted_risk_level']}
Confidence: {assessment['confidence']:.2%}

Risk Probabilities:
  - Low Risk:    {assessment['risk_probability'][0]:.2%}
  - Medium Risk: {assessment['risk_probability'][1]:.2%}
  - High Risk:   {assessment['risk_probability'][2]:.2%}

Recommendation: {assessment['recommendation']}

Connected Entities (Sample):
  Neighbors: {', '.join([str(n) for n in assessment['neighbors']])}
  Their Risk Levels: {', '.join(assessment['neighbor_risks'])}

Key Risk Factors:
"""
        for factor_name, factor_data in assessment['factors'].items():
            report += f"  - {factor_name}: {factor_data['value']:.4f} (Importance: {factor_data['importance_score']:.4f})\n"
        
        report += "\n" + "═" * 60 + "\n"
        
        return report
    
    def get_assessment_summary(self) -> Dict:
        """Get summary of all assessments performed."""
        if not self.assessment_history:
            return {'total_assessments': 0}
        
        risk_counts = {level.name: 0 for level in RiskLevel}
        total_confidence = 0
        
        for assessment in self.assessment_history:
            risk_counts[assessment['predicted_risk_level']] += 1
            total_confidence += assessment['confidence']
        
        return {
            'total_assessments': len(self.assessment_history),
            'risk_distribution': risk_counts,
            'average_confidence': total_confidence / len(self.assessment_history),
            'approval_rate': risk_counts['LOW'] / len(self.assessment_history) if self.assessment_history else 0
        }
