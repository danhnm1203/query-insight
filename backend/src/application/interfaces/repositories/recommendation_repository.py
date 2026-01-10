"""Interface for Recommendation repository."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.recommendation import Recommendation, RecommendationStatus


class IRecommendationRepository(ABC):
    """Interface for managing recommendation persistence."""

    @abstractmethod
    async def get_by_id(self, recommendation_id: UUID) -> Optional[Recommendation]:
        """Fetch a recommendation by its ID."""
        pass

    @abstractmethod
    async def get_by_query_id(self, query_id: UUID) -> List[Recommendation]:
        """Fetch all recommendations for a specific query."""
        pass

    @abstractmethod
    async def get_by_database_id(
        self, database_id: UUID, status: Optional[RecommendationStatus] = None
    ) -> List[Recommendation]:
        """Fetch all recommendations for a specific database."""
        pass

    @abstractmethod
    async def save(self, recommendation: Recommendation) -> Recommendation:
        """Save a recommendation."""
        pass

    @abstractmethod
    async def save_all(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """Save multiple recommendations."""
        pass

    @abstractmethod
    async def update_status(self, recommendation_id: UUID, status: RecommendationStatus) -> None:
        """Update the status of a recommendation."""
        pass
