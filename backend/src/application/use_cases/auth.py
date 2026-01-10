"""Registration and login use cases."""
from typing import Optional
from uuid import uuid4

from src.application.dto.user_dto import UserCreate, UserLogin, UserRead, Token
from src.application.interfaces.repositories.user_repository import IUserRepository
from src.application.services.security import hash_password, verify_password, create_access_token
from src.domain.entities.user import User


class RegistrationUseCase:
    """UseCase for registering a new user."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_create: UserCreate) -> UserRead:
        """Execute the registration."""
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_create.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user entity
        user = User(
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
            full_name=user_create.full_name,
            user_id=uuid4()
        )

        # Save to repository
        saved_user = await self.user_repo.save(user)
        
        return UserRead.model_validate(saved_user)


class LoginUseCase:
    """UseCase for authenticating a user and generating a token."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_login: UserLogin) -> Token:
        """Execute login and return JWT token."""
        user = await self.user_repo.get_by_email(user_login.email)
        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(user_login.password, user.hashed_password):
            raise ValueError("Invalid email or password")

        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": str(user.id)}
        )
        
        return Token(access_token=access_token)
