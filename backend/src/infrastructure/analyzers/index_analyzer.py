"""Index recommendation engine for generating CREATE INDEX suggestions."""
import re
from typing import Any, Dict, List, Optional, Set

from src.domain.entities.recommendation import RecommendationType

class IndexAnalyzer:
    """Analyzer for generating index suggestions based on query structure."""

    def analyze(self, sql_text: str, explain_findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze a query and its EXPLAIN findings to recommend indexes.
        
        Args:
            sql_text: Original SQL query text
            explain_findings: Findings from ExplainAnalyzer
        """
        recommendations = []
        
        # We focus on Seq Scans from the ExplainAnalyzer
        seq_scan_findings = [f for f in explain_findings if "Sequential Scan detected" in f["title"]]
        
        for finding in seq_scan_findings:
            node = finding["node_details"]
            table_name = node.get("Relation Name")
            filter_text = node.get("Filter", "")
            
            if not table_name:
                continue
                
            # Extract columns from the filter clause
            # Simple regex to find column names in filters like "(id > 1000)" or "(name = 'test')"
            # This is a PoC; a real production app should use a SQL parser like sqlglot or pglast
            columns = self._extract_columns_from_filter(filter_text)
            
            if columns:
                index_cols = ", ".join(columns)
                index_name = f"idx_{table_name}_{'_'.join(columns)}"[:63] # PostgreSQL limit
                
                sql_suggestion = f"CREATE INDEX {index_name} ON {table_name} ({index_cols});"
                
                recommendations.append({
                    "type": RecommendationType.INDEX,
                    "title": f"Add missing index on {table_name}",
                    "description": (
                        f"Adding an index on {table_name}({index_cols}) will convert the "
                        f"Sequential Scan into an Index Scan, significantly reducing query cost."
                    ),
                    "sql_suggestion": sql_suggestion,
                    "estimated_impact": 90.0,  # High impact estimated
                    "confidence": 0.85
                })
        
        return recommendations

    def _extract_columns_from_filter(self, filter_text: str) -> List[str]:
        """
        Extract potential column names from a PostgreSQL filter string.
        Example filter: "(id > 1000)" -> ["id"]
        Example filter: "((name = 'test'::text) AND (age > 18))" -> ["name", "age"]
        """
        if not filter_text:
            return []
            
        # Remove parenthesized casts like '::text' or '::integer'
        clean_text = re.sub(r'::\w+', '', filter_text)
        
        # Find identifiers followed by comparison operators ( =, >, <, >=, <=, !=, <>, LIKE, ILIKE, IN )
        # This regex looks for common patterns in PostgreSQL EXPLAIN output
        pattern = r'(\w+)\s*(?:[=><!]+|LIKE|ILIKE|IN)\s*'
        matches = re.findall(pattern, clean_text, re.IGNORECASE)
        
        # Deduplicate and return
        unique_cols = []
        seen = set()
        for col in matches:
            col_lower = col.lower()
            if col_lower not in seen and col_lower not in ("and", "or", "not", "null"):
                unique_cols.append(col_lower)
                seen.add(col_lower)
                
        return unique_cols
