"""Security dependencies for FastAPI."""
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.user_dto import TokenData
from src.application.interfaces.repositories.user_repository import IUserRepository
from src.application.services.security import decode_token
from src.domain.entities.user import User
from src.infrastructure.database.repositories.user_repository import PostgresUserRepository
from src.infrastructure.database.session import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> IUserRepository:
    """Dependency to get user repository."""
    return PostgresUserRepository(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: IUserRepository = Depends(get_user_repository)
) -> User:
    """Dependency to get authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        if email is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(email=email, user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = await user_repo.get_by_id(UUID(token_data.user_id))
    if user is None:
        raise credentials_exception
    
    # Add user context to Sentry
    import sentry_sdk
    sentry_sdk.set_user({"id": str(user.id), "email": user.email})
    
    return user
