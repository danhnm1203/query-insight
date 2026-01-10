"""SQLAlchemy implementation of database repository."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.database_repository import IDatabaseRepository
from src.domain.entities.database import Database, DatabaseType
from src.infrastructure.database.models import DatabaseModel


class PostgresDatabaseRepository(IDatabaseRepository):
    """PostgreSQL implementation of IDatabaseRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, db_id: UUID) -> Optional[Database]:
        """Get database by ID."""
        result = await self.session.execute(
            select(DatabaseModel).where(DatabaseModel.id == db_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_user_id(self, user_id: UUID) -> List[Database]:
        """Get all databases for a specific user."""
        result = await self.session.execute(
            select(DatabaseModel).where(DatabaseModel.user_id == user_id)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_all_active(self) -> List[Database]:
        """Get all active databases for background collection."""
        result = await self.session.execute(
            select(DatabaseModel).where(DatabaseModel.is_active == True)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def save(self, database: Database) -> Database:
        """Save a new database or update an existing one."""
        # Check if database already exists in DB
        result = await self.session.execute(
            select(DatabaseModel).where(DatabaseModel.id == database.id)
        )
        model = result.scalar_one_or_none()

        if model:
            # Update existing model
            model.name = database.name
            model.type = database.type
            model.encrypted_connection_string = database.encrypted_connection_string
            model.is_active = database.is_active
            model.last_connected_at = database.last_connected_at
        else:
            # Create new model
            model = DatabaseModel(
                id=database.id,
                user_id=database.user_id,
                name=database.name,
                type=database.type,
                encrypted_connection_string=database.encrypted_connection_string,
                is_active=database.is_active,
                created_at=database.created_at,
                last_connected_at=database.last_connected_at
            )
            self.session.add(model)

        await self.session.flush()
        return database

    async def delete(self, db_id: UUID) -> None:
        """Delete a database."""
        result = await self.session.execute(
            select(DatabaseModel).where(DatabaseModel.id == db_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()

    def _to_entity(self, model: DatabaseModel) -> Database:
        """Convert DatabaseModel to Database entity."""
        return Database(
            user_id=model.user_id,
            name=model.name,
            db_type=model.type,
            encrypted_connection_string=model.encrypted_connection_string,
            is_active=model.is_active,
            database_id=model.id
        )
