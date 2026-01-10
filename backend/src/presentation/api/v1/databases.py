"""Database management API routes."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.database_dto import DatabaseCreate, DatabaseRead
from src.application.use_cases.databases import RegisterDatabaseUseCase, GetDatabasesUseCase
from src.application.use_cases.test_connection import TestDatabaseConnectionUseCase
from src.domain.entities.user import User
from src.infrastructure.database.repositories.database_repository import PostgresDatabaseRepository
from src.infrastructure.database.session import get_db_session
from src.presentation.api.v1.deps import get_current_user

router = APIRouter(prefix="/databases", tags=["databases"])


@router.post("/test-connection")
async def test_connection(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Test a database connection."""
    db_repo = PostgresDatabaseRepository(db)
    use_case = TestDatabaseConnectionUseCase(db_repo)
    
    connection_string = payload.get("connection_string")
    db_type = payload.get("type", "postgres")
    
    if not connection_string:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Connection string is required"
        )
        
    is_valid = await use_case.execute(connection_string, db_type)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not establish connection to the database"
        )
        
    return {"status": "success", "message": "Connection established successfully"}


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


@router.delete("/{database_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_database(
    database_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Delete a database."""
    from src.application.use_cases.databases import DeleteDatabaseUseCase
    
    db_repo = PostgresDatabaseRepository(db)
    use_case = DeleteDatabaseUseCase(db_repo)
    
    try:
        await use_case.execute(current_user.id, database_id)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this database"
        )
