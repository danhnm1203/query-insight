"""Basic query analyzer for queries without EXPLAIN plans."""
import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class BasicQueryAnalyzer:
    """Analyze queries using pattern matching when EXPLAIN is unavailable."""
    
    def analyze(self, sql_text: str, execution_time_ms: float) -> List[Dict]:
        """
        Generate basic recommendations based on query text patterns.
        
        Checks for:
        - SELECT * usage
        - Missing LIMIT clauses
        - Missing WHERE clauses
        - Inefficient patterns
        
        Args:
            sql_text: SQL query text
            execution_time_ms: Query execution time in milliseconds
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Normalize SQL for analysis
        sql_upper = sql_text.upper()
        
        # Check for SELECT *
        if re.search(r'SELECT\s+\*', sql_text, re.IGNORECASE):
            recommendations.append({
                "type": "REWRITE",
                "title": "Avoid SELECT *",
                "description": "Selecting all columns can be inefficient. Specify only the columns you need to reduce data transfer and improve performance.",
                "sql_suggestion": None,
                "estimated_impact": 15.0,
                "confidence": 0.7
            })
        
        # Check for missing LIMIT on potentially large result sets
        if not re.search(r'\bLIMIT\b', sql_upper):
            if execution_time_ms > 100:  # Slow query without LIMIT
                recommendations.append({
                    "type": "LIMIT",
                    "title": "Add LIMIT clause",
                    "description": f"Query took {execution_time_ms:.0f}ms without a LIMIT clause. This may return too many rows. Consider adding LIMIT to paginate results.",
                    "sql_suggestion": None,
                    "estimated_impact": 25.0,
                    "confidence": 0.6
                })
        
        # Check for missing WHERE clause (full table scan likely)
        if not re.search(r'\bWHERE\b', sql_upper):
            if 'FROM' in sql_upper and execution_time_ms > 50:
                recommendations.append({
                    "type": "REWRITE",
                    "title": "Missing WHERE clause",
                    "description": "Query has no WHERE clause and may be scanning the entire table. Add filtering conditions to improve performance.",
                    "sql_suggestion": None,
                    "estimated_impact": 40.0,
                    "confidence": 0.8
                })
        
        # Check for LIKE with leading wildcard
        if re.search(r"LIKE\s+['\"]%", sql_text, re.IGNORECASE):
            recommendations.append({
                "type": "INDEX",
                "title": "Inefficient LIKE pattern",
                "description": "LIKE queries with leading wildcards (LIKE '%...') cannot use indexes efficiently. Consider using full-text search or restructuring the query.",
                "sql_suggestion": None,
                "estimated_impact": 30.0,
                "confidence": 0.75
            })
        
        # Check for OR conditions (may prevent index usage)
        or_count = len(re.findall(r'\bOR\b', sql_upper))
        if or_count > 2:
            recommendations.append({
                "type": "REWRITE",
                "title": "Multiple OR conditions",
                "description": f"Query has {or_count} OR conditions which may prevent efficient index usage. Consider using IN clause or UNION instead.",
                "sql_suggestion": None,
                "estimated_impact": 20.0,
                "confidence": 0.65
            })
        
        # Check for subqueries in SELECT clause
        if re.search(r'SELECT.*\(SELECT', sql_text, re.IGNORECASE | re.DOTALL):
            recommendations.append({
                "type": "REWRITE",
                "title": "Subquery in SELECT clause",
                "description": "Subqueries in SELECT clause execute for each row. Consider using JOINs or window functions instead.",
                "sql_suggestion": None,
                "estimated_impact": 35.0,
                "confidence": 0.7
            })
        
        # Check for DISTINCT without ORDER BY (may indicate data quality issue)
        if 'DISTINCT' in sql_upper and 'ORDER BY' not in sql_upper:
            if execution_time_ms > 100:
                recommendations.append({
                    "type": "REWRITE",
                    "title": "DISTINCT without ORDER BY",
                    "description": "DISTINCT can be expensive. Ensure it's necessary and consider adding ORDER BY for consistent results.",
                    "sql_suggestion": None,
                    "estimated_impact": 15.0,
                    "confidence": 0.5
                })
        
        logger.info(f"Generated {len(recommendations)} basic recommendations for query")
        return recommendations
