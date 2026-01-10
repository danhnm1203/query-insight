"""Query repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.query import Query


class IQueryRepository(ABC):
    """Interface for query repository."""

    @abstractmethod
    async def get_by_id(self, query_id: UUID) -> Optional[Query]:
        """Get query by ID."""
        pass

    @abstractmethod
    async def get_by_database_id(self, db_id: UUID, limit: int = 50) -> List[Query]:
        """Get latest queries for a specific database."""
        pass

    @abstractmethod
    async def save(self, query: Query) -> Query:
        """Save a new query or update an existing one."""
        pass

    @abstractmethod
    async def save_all(self, queries: List[Query]) -> List[Query]:
        """Save multiple queries."""
        pass

    @abstractmethod
    async def get_aggregated_metrics(self, db_id: UUID, hours: int = 24) -> List[dict]:
        """Get aggregated metrics grouped by normalized_sql."""
        pass
