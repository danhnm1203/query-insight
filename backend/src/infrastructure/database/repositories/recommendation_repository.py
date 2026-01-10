"""PostgreSQL implementation of Recommendation repository."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.recommendation_repository import IRecommendationRepository
from src.domain.entities.recommendation import Recommendation, RecommendationStatus
from src.infrastructure.database.models import RecommendationModel, QueryModel


class PostgresRecommendationRepository(IRecommendationRepository):
    """PostgreSQL implementation for managing recommendation persistence."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, recommendation_id: UUID) -> Optional[Recommendation]:
        """Fetch a recommendation by its ID."""
        result = await self.session.execute(
            select(RecommendationModel).where(RecommendationModel.id == recommendation_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_query_id(self, query_id: UUID) -> List[Recommendation]:
        """Fetch all recommendations for a specific query."""
        result = await self.session.execute(
            select(RecommendationModel).where(RecommendationModel.query_id == query_id)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_by_database_id(
        self, database_id: UUID, status: Optional[RecommendationStatus] = None
    ) -> List[Recommendation]:
        """Fetch all recommendations for a specific database."""
        stmt = (
            select(RecommendationModel)
            .join(QueryModel)
            .where(QueryModel.database_id == database_id)
        )
        if status:
            stmt = stmt.where(RecommendationModel.status == status)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def save(self, recommendation: Recommendation) -> Recommendation:
        """Save a recommendation."""
        model = RecommendationModel(
            id=recommendation.id,
            query_id=recommendation.query_id,
            type=recommendation.type,
            title=recommendation.title,
            description=recommendation.description,
            sql_suggestion=recommendation.sql_suggestion,
            estimated_impact=recommendation.estimated_impact,
            confidence=recommendation.confidence,
            status=recommendation.status,
            created_at=recommendation.created_at,
            applied_at=recommendation.applied_at,
        )
        self.session.add(model)
        await self.session.flush()
        return recommendation

    async def save_all(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """Save multiple recommendations."""
        for rec in recommendations:
            await self.save(rec)
        return recommendations

    async def update_status(self, recommendation_id: UUID, status: RecommendationStatus) -> None:
        """Update the status of a recommendation."""
        await self.session.execute(
            update(RecommendationModel)
            .where(RecommendationModel.id == recommendation_id)
            .values(status=status)
        )

    def _to_entity(self, model: RecommendationModel) -> Recommendation:
        """Convert SQLAlchemy model to domain entity."""
        return Recommendation(
            recommendation_id=model.id,
            query_id=model.query_id,
            rec_type=model.type,
            title=model.title,
            description=model.description,
            sql_suggestion=model.sql_suggestion,
            estimated_impact=model.estimated_impact,
            confidence=model.confidence,
            status=model.status,
        )
