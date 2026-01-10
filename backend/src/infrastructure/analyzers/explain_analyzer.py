"""EXPLAIN plan analyzer for identifying performance bottlenecks."""
import logging
from typing import Any, Dict, List, Optional

from src.domain.entities.recommendation import RecommendationType

logger = logging.getLogger(__name__)

class ExplainAnalyzer:
    """Analyzer for PostgreSQL EXPLAIN plans."""

    def analyze(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze an EXPLAIN plan and return a list of findings.
        
        Args:
            plan: The 'Plan' object from PostgreSQL EXPLAIN (FORMAT JSON)
        """
        findings = []
        
        # Start recursive analysis of the plan tree
        self._analyze_node(plan.get("Plan", plan), findings)
        
        return findings

    def _analyze_node(self, node: Dict[str, Any], findings: List[Dict[str, Any]]):
        """Recursively analyze nodes in the plan tree."""
        node_type = node.get("Node Type")
        
        # 1. Detect Sequential Scans on large tables
        if node_type == "Seq Scan":
            # For the PoC, we consider anything over 1000 rows as "large" for a Seq Scan
            # In a real app, this threshold would be configurable or based on cost
            plan_rows = node.get("Plan Rows", 0)
            if plan_rows > 1000:
                findings.append({
                    "type": RecommendationType.INDEX,
                    "title": f"Sequential Scan detected on {node.get('Relation Name')}",
                    "description": (
                        f"The query is performing a sequential scan on {node.get('Relation Name')} "
                        f"which is estimated to have {plan_rows} rows. Adding an index on the "
                        f"filter columns ({node.get('Filter', 'N/A')}) might improve performance."
                    ),
                    "impact": 0.8,  # High impact
                    "confidence": 0.7,
                    "node_details": node
                })

        # 2. Detect Nested Loops on large results
        if node_type == "Nested Loop":
            actual_rows = node.get("Actual Rows", 0)
            if actual_rows > 5000:
                findings.append({
                    "type": RecommendationType.REWRITE,
                    "title": "Large Nested Loop detected",
                    "description": (
                        f"A nested loop join produced {actual_rows} rows. This often indicates "
                        "that a Hash Join or Merge Join would be more efficient, possibly "
                        "due to missing indexes or outdated statistics."
                    ),
                    "impact": 0.6,
                    "confidence": 0.6,
                    "node_details": node
                })

        # 3. Detect high cost nodes
        total_cost = node.get("Total Cost", 0)
        if total_cost > 10000:
            findings.append({
                "type": RecommendationType.SCALING,
                "title": "High cost operation detected",
                "description": (
                    f"A {node_type} operation has a high estimated cost of {total_cost}. "
                    "This might be a candidate for optimization or architectural changes."
                ),
                "impact": 0.4,
                "confidence": 0.5,
                "node_details": node
            })

        # Recursively analyze children
        if "Plans" in node:
            for child in node["Plans"]:
                self._analyze_node(child, findings)
