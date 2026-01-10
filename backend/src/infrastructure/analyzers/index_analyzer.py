"""Index recommendation engine for generating CREATE INDEX suggestions."""
import re
from typing import Any, Dict, List, Optional, Set

from src.domain.entities.recommendation import RecommendationType

from src.domain.entities.recommendation import RecommendationType

class IndexAnalyzer:
    """Production-ready index recommendation engine."""

    def analyze(self, sql_text: str, explain_findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze a query and its EXPLAIN findings to recommend indexes.
        
        Args:
            sql_text: Original SQL query text
            explain_findings: Findings from ExplainAnalyzer
        """
        recommendations = []
        
        # We focus on Seq Scans and Sorts from the ExplainAnalyzer
        for finding in explain_findings:
            node = finding["node_details"]
            node_type = node.get("Node Type")
            
            if node_type == "Seq Scan":
                table_name = node.get("Relation Name")
                filter_text = node.get("Filter", "")
                
                if not table_name:
                    continue
                    
                columns = self._extract_columns_from_filter(filter_text)
                if columns:
                    recommendations.append(self._create_index_rec(table_name, columns, "cost reduction"))
            
            elif node_type == "Sort":
                # Check for Sort Key
                sort_keys = node.get("Sort Key", [])
                # If there's a child Seq Scan, we can optimize the sort by adding an index
                # This is a simplification; in reality, we'd check the entire branch
                table_name = self._find_target_table(node)
                if table_name and sort_keys:
                    columns = self._extract_columns_from_sort_keys(sort_keys)
                    if columns:
                        recommendations.append(self._create_index_rec(table_name, columns, "sort optimization"))
        
        # Deduplicate recommendations by title
        unique_recs = []
        seen_titles = set()
        for rec in recommendations:
            if rec["title"] not in seen_titles:
                unique_recs.append(rec)
                seen_titles.add(rec["title"])
                
        return unique_recs

    def _create_index_rec(self, table_name: str, columns: List[str], reason: str) -> Dict[str, Any]:
        """Helper to create a recommendation dictionary."""
        index_cols = ", ".join(columns)
        index_name = f"idx_{table_name}_{'_'.join(columns)}"[:63]
        sql = f"CREATE INDEX {index_name} ON {table_name} ({index_cols});"
        
        return {
            "type": RecommendationType.INDEX,
            "title": f"Add index on {table_name} ({index_cols})",
            "description": (
                f"Adding an index on {table_name} using columns ({index_cols}) will help with {reason}. "
                "This can convert expensive sequential operations into efficient index lookups."
            ),
            "sql_suggestion": sql,
            "estimated_impact": 80.0,
            "confidence": 0.85
        }

    def _extract_columns_from_filter(self, filter_text: str) -> List[str]:
        """Extract potential column names from a PostgreSQL filter string."""
        if not filter_text:
            return []
            
        import re
        # Remove casts and find identifiers
        clean_text = re.sub(r'::\w+', '', filter_text)
        pattern = r'(\w+)\s*(?:[=><!]+|LIKE|ILIKE|IN)\s*'
        matches = re.findall(pattern, clean_text, re.IGNORECASE)
        
        unique_cols = []
        seen = set()
        for col in matches:
            c = col.lower()
            if c not in seen and c not in ("and", "or", "not", "null"):
                unique_cols.append(c)
                seen.add(c)
        return unique_cols

    def _extract_columns_from_sort_keys(self, sort_keys: Any) -> List[str]:
        """Extract column names from sort keys (e.g. ['(id DESC)', 'name'])."""
        import re
        cols = []
        keys = [sort_keys] if isinstance(sort_keys, str) else sort_keys
        for key in keys:
            # Match first word that looks like an identifier
            match = re.search(r'(\w+)', key)
            if match:
                cols.append(match.group(1).lower())
        return cols

    def _find_target_table(self, node: Dict[str, Any]) -> Optional[str]:
        """Recursively search for a Relation Name in the children of a node."""
        if "Relation Name" in node:
            return node["Relation Name"]
        
        if "Plans" in node:
            for child in node["Plans"]:
                table = self._find_target_table(child)
                if table:
                    return table
        return None
