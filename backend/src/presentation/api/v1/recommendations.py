"""Recommendations API routes."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.manage_recommendations import UpdateRecommendationStatusUseCase
from src.domain.entities.user import User
from src.domain.entities.recommendation import RecommendationStatus
from src.infrastructure.database.repositories.recommendation_repository import PostgresRecommendationRepository
from src.infrastructure.database.session import get_db_session
from src.presentation.api.v1.deps import get_current_user

router = APIRouter(tags=["recommendations"])

@router.post("/recommendations/{recommendation_id}/apply")
async def apply_recommendation(
    recommendation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Mark a recommendation as applied."""
    rec_repo = PostgresRecommendationRepository(db)
    use_case = UpdateRecommendationStatusUseCase(rec_repo)
    await use_case.execute(recommendation_id, RecommendationStatus.APPLIED)
    return {"status": "success", "message": "Recommendation marked as applied"}

@router.post("/recommendations/{recommendation_id}/dismiss")
async def dismiss_recommendation(
    recommendation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Mark a recommendation as dismissed."""
    rec_repo = PostgresRecommendationRepository(db)
    use_case = UpdateRecommendationStatusUseCase(rec_repo)
    await use_case.execute(recommendation_id, RecommendationStatus.DISMISSED)
    return {"status": "success", "message": "Recommendation dismissed"}
