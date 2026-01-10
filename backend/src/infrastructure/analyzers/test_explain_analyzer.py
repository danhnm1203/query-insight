"""Test script for EXPLAIN Analyzer."""
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.infrastructure.analyzers.explain_analyzer import ExplainAnalyzer

def test_analyzer():
    print("🚀 Starting EXPLAIN Analyzer Test...")
    
    # Mock EXPLAIN plan with a Seq Scan on a large table
    mock_plan = {
        "Plan": {
            "Node Type": "Seq Scan",
            "Relation Name": "large_table",
            "Alias": "lt",
            "Startup Cost": 0.00,
            "Total Cost": 15000.00,
            "Plan Rows": 100000,
            "Plan Width": 256,
            "Filter": "(id > 1000)",
            "Plans": [
                {
                    "Node Type": "Nested Loop",
                    "Actual Rows": 6000,
                    "Total Cost": 5000.00,
                    "Plans": []
                }
            ]
        }
    }
    
    analyzer = ExplainAnalyzer()
    findings = analyzer.analyze(mock_plan)
    
    print(f"\nFound {len(findings)} issues in the plan:")
    
    for i, finding in enumerate(findings):
        print(f"\n[{i+1}] {finding['title']} ({finding['type']})")
        print(f"    Impact: {finding['impact']}, Confidence: {finding['confidence']}")
        print(f"    Description: {finding['description']}")

if __name__ == "__main__":
    test_analyzer()
