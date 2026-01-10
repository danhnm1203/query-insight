"""Database management API routes."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.database_dto import DatabaseCreate, DatabaseRead
from src.application.use_cases.databases import RegisterDatabaseUseCase, GetDatabasesUseCase
from src.domain.entities.user import User
from src.infrastructure.database.repositories.database_repository import PostgresDatabaseRepository
from src.infrastructure.database.session import get_db_session
from src.presentation.api.v1.deps import get_current_user

router = APIRouter(prefix="/databases", tags=["databases"])


@router.post("", response_model=DatabaseRead, status_code=status.HTTP_201_CREATED)
async def register_database(
    db_create: DatabaseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Register a new database for the current user."""
    db_repo = PostgresDatabaseRepository(db)
    use_case = RegisterDatabaseUseCase(db_repo)
    return await use_case.execute(current_user.id, db_create)


@router.get("", response_model=List[DatabaseRead])
async def get_databases(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get all databases registered by the current user."""
    db_repo = PostgresDatabaseRepository(db)
    use_case = GetDatabasesUseCase(db_repo)
    return await use_case.execute(current_user.id)
