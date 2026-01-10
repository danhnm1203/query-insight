"""Metrics API routes."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.metric_dto import MetricsResponse
from src.application.use_cases.get_metrics import GetMetricsUseCase
from src.domain.entities.user import User
from src.infrastructure.database.repositories.metric_repository import PostgresMetricRepository
from src.infrastructure.database.session import get_db_session
from src.presentation.api.v1.deps import get_current_user

router = APIRouter(prefix="/databases/{database_id}/metrics", tags=["metrics"])

@router.get("", response_model=MetricsResponse)
async def get_metrics(
    database_id: UUID,
    time_range: str = "1h",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get performance metrics for a specific database."""
    # Convert time_range string (e.g. "1h", "24h") to hours
    try:
        if time_range.endswith("h"):
            hours = int(time_range[:-1])
        elif time_range.endswith("d"):
            hours = int(time_range[:-1]) * 24
        else:
            hours = 1
    except ValueError:
        hours = 1

    metric_repo = PostgresMetricRepository(db)
    use_case = GetMetricsUseCase(metric_repo)
    
    return await use_case.execute(database_id, hours)
