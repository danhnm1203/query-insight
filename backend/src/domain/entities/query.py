"""Domain entities for QueryInsight."""
from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from uuid import UUID, uuid4


class QueryStatus(str, Enum):
    """Status of a query."""
    SLOW = "slow"
    NORMAL = "normal"
    OPTIMIZED = "optimized"
    ERROR = "error"


class Query:
    """Query entity representing a database query execution."""
    
    def __init__(
        self,
        database_id: UUID,
        sql_text: str,
        normalized_sql: str,
        execution_time_ms: float,
        timestamp: datetime,
        explain_plan: Optional[Dict] = None,
        status: QueryStatus = QueryStatus.SLOW,
        query_id: Optional[UUID] = None,
    ):
        self.id = query_id or uuid4()
        self.database_id = database_id
        self.sql_text = sql_text
        self.normalized_sql = normalized_sql
        self.execution_time_ms = execution_time_ms
        self.timestamp = timestamp
        self.explain_plan = explain_plan or {}
        self.status = status
        self.created_at = datetime.utcnow()
    
    def is_slow(self, threshold_ms: float = 1000) -> bool:
        """Check if query execution time exceeds threshold."""
        return self.execution_time_ms > threshold_ms
    
    def mark_as_optimized(self) -> None:
        """Mark query as optimized."""
        self.status = QueryStatus.OPTIMIZED
    
    def __repr__(self) -> str:
        return f"<Query {self.id} - {self.execution_time_ms}ms>"
