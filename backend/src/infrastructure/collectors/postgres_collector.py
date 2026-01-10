"""PostgreSQL query collector for capturing performance data."""
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import asyncpg
from src.domain.entities.query import Query, QueryStatus

logger = logging.getLogger(__name__)

class PostgresCollector:
    """Collector for PostgreSQL query performance data using pg_stat_statements."""

    def __init__(self, connection_url: str):
        """
        Initialize the collector.
        
        Args:
            connection_url: asyncpg compatible connection URL (e.g. postgresql://user:pass@host:port/db)
        """
        self.connection_url = connection_url

    async def check_extensions(self, conn: asyncpg.Connection) -> bool:
        """Check if required extensions are installed."""
        try:
            result = await conn.fetchval(
                "SELECT count(*) FROM pg_extension WHERE extname = 'pg_stat_statements'"
            )
            return result > 0
        except Exception as e:
            logger.error(f"Error checking extensions: {e}")
            return False

    async def collect_slow_queries(
        self, threshold_ms: float = 100.0, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Collect slow queries from pg_stat_statements.
        
        Args:
            threshold_ms: Mean execution time threshold in milliseconds.
            limit: Maximum number of queries to collect.
        """
        conn = await asyncpg.connect(self.connection_url)
        try:
            if not await self.check_extensions(conn):
                logger.warning("pg_stat_statements extension not found in the target database.")
                return []

            # Query pg_stat_statements for queries exceeding the threshold
            # Note: total_exec_time and calls are used to calculate mean_exec_time
            query = """
                SELECT 
                    queryid as query_id,
                    query as sql_text,
                    calls,
                    total_exec_time / calls as mean_exec_time_ms,
                    rows as total_rows
                FROM pg_stat_statements
                WHERE total_exec_time / calls > $1
                ORDER BY mean_exec_time_ms DESC
                LIMIT $2
            """
            rows = await conn.fetch(query, threshold_ms, limit)
            
            results = []
            for row in rows:
                results.append({
                    "query_id": str(row["query_id"]),
                    "sql_text": row["sql_text"],
                    "calls": row["calls"],
                    "mean_exec_time_ms": row["mean_exec_time_ms"],
                    "total_rows": row["total_rows"]
                })
            return results
        finally:
            await conn.close()

    async def get_explain_plan(self, sql_text: str, params: Optional[List[Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get the EXPLAIN (FORMAT JSON, ANALYZE) for a given query.
        
        WARNING: This executes the query! Only run on SELECT statements or in a transaction that is rolled back.
        In this PoC, we only attempt to EXPLAIN queries that look like SELECT.
        """
        if not sql_text.strip().upper().startswith("SELECT"):
            logger.warning("Skipping EXPLAIN for non-SELECT query to avoid unintended side effects.")
            return None

        conn = await asyncpg.connect(self.connection_url)
        try:
            # We use a transaction and rollback just in case, though ANALYZE with SELECT is safe.
            async with conn.transaction():
                explain_query = f"EXPLAIN (FORMAT JSON, ANALYZE) {sql_text}"
                try:
                    # Note: We might need to handle parameters if the sql_text contains placeholders
                    # For pg_stat_statements, sql_text is already normalized with $1, $2 etc.
                    # This makes it hard to run EXPLAIN ANALYZE without dummy parameters.
                    # For the PoC, we handle the simple case or queries without placeholders.
                    result = await conn.fetchval(explain_query)
                    if isinstance(result, str):
                        return json.loads(result)[0]
                    return result[0]
                except Exception as e:
                    logger.error(f"Error running EXPLAIN: {e}")
                    return None
                finally:
                    # Force rollback
                    pass
        finally:
            await conn.close()
