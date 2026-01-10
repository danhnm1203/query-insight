"""Metric repository interface."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID

from src.domain.entities.metric import Metric


class IMetricRepository(ABC):
    """Interface for metric repository."""

    @abstractmethod
    async def get_by_database_id(
        self, db_id: UUID, start_time: datetime, end_time: datetime
    ) -> List[Metric]:
        """Get metrics for a specific database and time range."""
        pass

    @abstractmethod
    async def save(self, metric: Metric) -> Metric:
        """Save a new metric."""
        pass

    @abstractmethod
    async def save_all(self, metrics: List[Metric]) -> List[Metric]:
        """Save multiple metrics."""
        pass
