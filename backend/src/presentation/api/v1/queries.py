"""Queries API routes."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.query_dto import QueryRead
from src.application.use_cases.get_queries import GetSlowQueriesUseCase, GetQueryDetailsUseCase
from src.domain.entities.user import User
from src.infrastructure.database.repositories.query_repository import PostgresQueryRepository
from src.infrastructure.database.session import get_db_session
from src.presentation.api.v1.deps import get_current_user

router = APIRouter(tags=["queries"])

@router.get("/databases/{database_id}/queries/slow", response_model=List[QueryRead])
async def get_slow_queries(
    database_id: UUID,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get latest slow queries for a specific database."""
    query_repo = PostgresQueryRepository(db)
    use_case = GetSlowQueriesUseCase(query_repo)
    return await use_case.execute(database_id, limit)

@router.get("/queries/{query_id}", response_model=QueryRead)
async def get_query_details(
    query_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get details for a specific query."""
    query_repo = PostgresQueryRepository(db)
    use_case = GetQueryDetailsUseCase(query_repo)
    query = await use_case.execute(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    return query
