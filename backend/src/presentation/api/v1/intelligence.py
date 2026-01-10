"""Intelligence API routes for patterns and trends."""
from typing import List, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.analyze_trends import AnalyzeTrendsUseCase
from src.domain.entities.user import User
from src.infrastructure.database.repositories.query_repository import PostgresQueryRepository
from src.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.database.session import get_db_session
from src.presentation.api.v1.deps import get_current_user

router = APIRouter(prefix="/databases/{database_id}/intelligence", tags=["intelligence"])

@router.get("/patterns")
async def get_query_patterns(
    database_id: UUID,
    hours: int = 24,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get most frequent query patterns (fingerprints) for a database."""
    query_repo = PostgresQueryRepository(db)
    return await query_repo.get_aggregated_metrics(database_id, hours=hours)

@router.get("/trends")
async def get_performance_trends(
    database_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get detected performance regressions and trends."""
    uow = SqlAlchemyUnitOfWork(db)
    use_case = AnalyzeTrendsUseCase(uow)
    return await use_case.execute(database_id)
