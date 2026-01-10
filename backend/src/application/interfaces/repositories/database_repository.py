"""Database repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.database import Database


class IDatabaseRepository(ABC):
    """Interface for database repository."""

    @abstractmethod
    async def get_by_id(self, db_id: UUID) -> Optional[Database]:
        """Get database by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Database]:
        """Get all databases for a specific user."""
        pass

    @abstractmethod
    async def get_all_active(self) -> List[Database]:
        """Get all active databases for background collection."""
        pass

    @abstractmethod
    async def save(self, database: Database) -> Database:
        """Save a new database or update an existing one."""
        pass

    @abstractmethod
    async def delete(self, db_id: UUID) -> None:
        """Delete a database."""
        pass
