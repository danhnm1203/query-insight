"""EXPLAIN plan analyzer for identifying performance bottlenecks."""
import logging
from typing import Any, Dict, List, Optional

from src.domain.entities.recommendation import RecommendationType

logger = logging.getLogger(__name__)

class ExplainAnalyzer:
    """Production-ready analyzer for PostgreSQL EXPLAIN plans (JSON format)."""

    def analyze(self, plan_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze an EXPLAIN plan and return a list of performance findings.
        
        Args:
            plan_data: The full JSON output from EXPLAIN (FORMAT JSON, ANALYZE)
        """
        findings = []
        
        # PostgreSQL puts the plan under a "Plan" key in the first element of the list
        plan = plan_data.get("Plan", plan_data)
        if isinstance(plan_data, list) and plan_data:
            plan = plan_data[0].get("Plan", plan_data[0])

        self._analyze_node(plan, findings)
        
        # Sort findings by impact (descending)
        findings.sort(key=lambda x: x["impact"], reverse=True)
        return findings

    def _analyze_node(self, node: Dict[str, Any], findings: List[Dict[str, Any]]):
        """Recursively analyze nodes in the plan tree."""
        node_type = node.get("Node Type")
        
        # 1. Sequential Scans on large tables
        if node_type == "Seq Scan":
            plan_rows = node.get("Plan Rows", 0)
            if plan_rows > 1000:
                findings.append({
                    "type": RecommendationType.INDEX,
                    "title": f"Sequential Scan on {node.get('Relation Name')}",
                    "description": (
                        f"The query is performing a full table scan on {node.get('Relation Name')}. "
                        f"Estimated {plan_rows} rows will be processed. Adding an index could "
                        "significantly speed up this operation."
                    ),
                    "impact": self._calculate_impact(node, weight=0.8),
                    "confidence": 0.9,
                    "node_details": node
                })

        # 2. Large Nested Loops
        elif node_type == "Nested Loop":
            actual_rows = node.get("Actual Rows", node.get("Plan Rows", 0))
            if actual_rows > 5000:
                findings.append({
                    "type": RecommendationType.REWRITE,
                    "title": "Expensive Nested Loop Join",
                    "description": (
                        f"A Nested Loop join is processing {actual_rows} rows. This is often "
                        "inefficient for large datasets. Consider using a Hash Join or Merge Join "
                        "by ensuring indexes are available on join columns."
                    ),
                    "impact": self._calculate_impact(node, weight=0.7),
                    "confidence": 0.75,
                    "node_details": node
                })

        # 3. Mismatched Statistics (Outdated Stats)
        plan_rows = node.get("Plan Rows", 0)
        actual_rows = node.get("Actual Rows", None)
        if actual_rows is not None and plan_rows > 0:
            ratio = max(actual_rows, 1) / max(plan_rows, 1)
            if ratio > 10 or ratio < 0.1:
                findings.append({
                    "type": RecommendationType.SCHEMA_CHANGE,
                    "title": f"Outdated Statistics for {node.get('Relation Name', node_type)}",
                    "description": (
                        f"The query planner estimated {plan_rows} rows but actually processed {actual_rows}. "
                        "Stale statistics can lead to poor execution plans. Running ANALYZE on this "
                        "table is recommended."
                    ),
                    "impact": 0.5,
                    "confidence": 0.8,
                    "node_details": node
                })

        # 4. Sorting in Memory (Large Sorts)
        if node_type == "Sort":
            actual_rows = node.get("Actual Rows", node.get("Plan Rows", 0))
            if actual_rows > 10000:
                findings.append({
                    "type": RecommendationType.INDEX,
                    "title": f"Large Memory Sort ({actual_rows} rows)",
                    "description": (
                        "The query is sorting a large amount of data in memory. An index on the "
                        "ORDER BY columns could eliminate the need for an explicit sort."
                    ),
                    "impact": self._calculate_impact(node, weight=0.6),
                    "confidence": 0.85,
                    "node_details": node
                })

        # Recursively analyze children
        if "Plans" in node:
            for child in node["Plans"]:
                self._analyze_node(child, findings)

    def _calculate_impact(self, node: Dict[str, Any], weight: float) -> float:
        """Calculate a normalized impact score (0-1)."""
        # Base impact from cost
        total_cost = node.get("Total Cost", 0)
        # Logarithmic scaling for cost to keep impact sensible
        # A cost of 1000 -> approx 0.3, 100,000 -> approx 0.8
        import math
        cost_score = min(math.log10(max(total_cost, 1)) / 6, 1.0)
        
        return round(cost_score * weight, 2)
