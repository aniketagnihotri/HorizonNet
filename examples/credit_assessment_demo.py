"""
Credit Entity GAT System - Complete Example
Demonstrates end-to-end workflow for credit entity risk assessment.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from horizonnet import CreditEntityDataset, CreditEntityGraph, GAT, CreditAssessmentAgent


def main():
    """Main example execution."""
    
    print("=" * 70)
    print("HORIZONNET: CREDIT ENTITY GAT SYSTEM - DEMO")
    print("=" * 70)
    
    # Step 1: Create and prepare dataset
    print("\n[Step 1] Loading Credit Entity Dataset...")
    dataset = CreditEntityDataset(num_entities=50, seed=42)
    data = dataset.generate_synthetic_data()
    
    print(f"  ✓ Loaded {data['features'].shape[0]} entities")
    print(f"  ✓ Features per entity: {data['features'].shape[1]}")
    print(f"  ✓ Feature names: {', '.join(dataset.get_feature_names())}")
    print(f"  ✓ Risk distribution: {np.bincount(data['labels'])}")
    
    # Step 2: Build graph
    print("\n[Step 2] Building Credit Entity Graph...")
    graph = CreditEntityGraph(data['features'], similarity_threshold=0.6)
    edge_index, edge_weights = graph.build_knn_graph(k=5)
    adj_matrix = graph.get_adjacency_matrix()
    
    stats = graph.get_graph_statistics()
    print(f"  ✓ Number of nodes: {stats['num_nodes']}")
    print(f"  ✓ Number of edges: {stats['num_edges']}")
    print(f"  ✓ Graph density: {stats['density']:.4f}")
    print(f"  ✓ Average node degree: {stats['avg_degree']:.2f}")
    
    # Step 3: Initialize GAT model
    print("\n[Step 3] Initializing GAT Model...")
    model = GAT(
        in_features=data['features'].shape[1],
        hidden_features=[16, 8],
        num_classes=3,
        num_heads=1,
        dropout=0.1,
        learning_rate=0.01
    )
    
    print(model.summary())
    
    # Step 4: Create assessment agent
    print("\n[Step 4] Initializing Credit Assessment Agent...")
    agent = CreditAssessmentAgent(model, graph, dataset)
    print("  ✓ Agent ready for credit assessments")
    
    # Step 5: Perform individual assessments
    print("\n[Step 5] Performing Individual Entity Assessments...")
    print("-" * 70)
    
    test_entities = [0, 10, 25, 35, 45]
    
    for entity_idx in test_entities:
        assessment = agent.assess_entity(entity_idx, data['features'], adj_matrix)
        report = agent.generate_report(assessment)
        print(report)
    
    # Step 6: Batch assessment
    print("\n[Step 6] Batch Assessment of Multiple Entities...")
    batch_indices = list(range(0, 50, 5))
    batch_results = agent.assess_batch(batch_indices, data['features'], adj_matrix)
    
    print(f"  ✓ Assessed {len(batch_results)} entities in batch mode")
    
    # Step 7: Generate summary report
    print("\n[Step 7] Assessment Summary...")
    print("-" * 70)
    
    summary = agent.get_assessment_summary()
    
    print(f"Total Assessments: {summary['total_assessments']}")
    print(f"Risk Distribution:")
    for risk_level, count in summary['risk_distribution'].items():
        percentage = (count / summary['total_assessments'] * 100) if summary['total_assessments'] > 0 else 0
        print(f"  • {risk_level}: {count} ({percentage:.1f}%)")
    
    print(f"Average Confidence: {summary['average_confidence']:.2%}")
    print(f"Approval Rate: {summary['approval_rate']:.2%}")
    
    # Step 8: Model predictions
    print("\n[Step 8] Model Predictions Across All Entities...")
    print("-" * 70)
    
    all_predictions = model.predict(data['features'], adj_matrix)
    all_probabilities = model.predict_proba(data['features'], adj_matrix)
    
    unique, counts = np.unique(all_predictions, return_counts=True)
    print("Risk Level Distribution:")
    risk_names = ["LOW", "MEDIUM", "HIGH"]
    for risk_id, count in zip(unique, counts):
        print(f"  • {risk_names[risk_id]}: {count} entities")
    
    max_probs = np.max(all_probabilities, axis=1)
    high_confidence_idx = max_probs > 0.8
    print(f"\nHigh Confidence Predictions (>80%): {np.sum(high_confidence_idx)} entities")
    
    low_confidence_idx = max_probs < 0.5
    print(f"Low Confidence Predictions (<50%): {np.sum(low_confidence_idx)} entities")
    
    print("\n" + "=" * 70)
    print("✓ DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
