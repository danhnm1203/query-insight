"""User repository interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User


class IUserRepository(ABC):
    """Interface for user repository."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a new user or update an existing one."""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """Delete a user."""
        pass
