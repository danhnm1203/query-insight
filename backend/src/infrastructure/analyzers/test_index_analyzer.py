"""Test script for Index Recommendation Engine."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.infrastructure.analyzers.index_analyzer import IndexAnalyzer
from src.domain.entities.recommendation import RecommendationType

def test_index_analyzer():
    print("🚀 Starting Index Analyzer Test...")
    
    sql_text = "SELECT * FROM users WHERE email = 'test@example.com' AND age > 25;"
    
    # Mock findings from ExplainAnalyzer
    mock_explain_findings = [
        {
            "type": RecommendationType.INDEX,
            "title": "Sequential Scan detected on users",
            "description": "...",
            "node_details": {
                "Node Type": "Seq Scan",
                "Relation Name": "users",
                "Plan Rows": 10000,
                "Filter": "((email = 'test@example.com'::text) AND (age > 25))"
            }
        }
    ]
    
    analyzer = IndexAnalyzer()
    recommendations = analyzer.analyze(sql_text, mock_explain_findings)
    
    print(f"\nFound {len(recommendations)} recommendations:")
    
    for i, rec in enumerate(recommendations):
        print(f"\n[{i+1}] {rec['title']}")
        print(f"    Impact: {rec['estimated_impact']}%, Confidence: {rec['confidence']}")
        print(f"    Description: {rec['description']}")
        print(f"    SQL: {rec['sql_suggestion']}")

if __name__ == "__main__":
    test_index_analyzer()
