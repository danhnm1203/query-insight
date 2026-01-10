"""SQLAlchemy implementation of user repository."""
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.user_repository import IUserRepository
from src.domain.entities.user import User
from src.infrastructure.database.models import UserModel


class PostgresUserRepository(IUserRepository):
    """PostgreSQL implementation of IUserRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    async def save(self, user: User) -> User:
        """Save a new user or update an existing one."""
        # Check if user already exists in DB
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one_or_none()

        if user_model:
            # Update existing model
            user_model.email = user.email
            user_model.hashed_password = user.hashed_password
            user_model.full_name = user.full_name
            user_model.plan_tier = user.plan_tier
            user_model.is_active = user.is_active
            user_model.onboarding_completed = user.onboarding_completed
        else:
            # Create new model
            user_model = UserModel(
                id=user.id,
                email=user.email,
                hashed_password=user.hashed_password,
                full_name=user.full_name,
                plan_tier=user.plan_tier,
                is_active=user.is_active,
                onboarding_completed=user.onboarding_completed,
                created_at=user.created_at
            )
            self.session.add(user_model)

        await self.session.flush()
        return user

    async def delete(self, user_id: UUID) -> None:
        """Delete a user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model:
            await self.session.delete(user_model)
            await self.session.flush()

    def _to_entity(self, model: UserModel) -> User:
        """Convert UserModel to User entity."""
        return User(
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            plan_tier=model.plan_tier,
            is_active=model.is_active,
            onboarding_completed=model.onboarding_completed,
            user_id=model.id
        )
