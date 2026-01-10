"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.user_dto import UserCreate, UserLogin, UserRead, Token
from src.application.use_cases.auth import RegistrationUseCase, LoginUseCase
from src.domain.entities.user import User
from src.infrastructure.database.repositories.user_repository import PostgresUserRepository
from src.infrastructure.database.session import get_db_session
from src.presentation.api.v1.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Register a new user."""
    user_repo = PostgresUserRepository(db)
    use_case = RegistrationUseCase(user_repo)
    try:
        return await use_case.execute(user_create)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db_session)
):
    """Authenticate and get access token."""
    user_repo = PostgresUserRepository(db)
    use_case = LoginUseCase(user_repo)
    try:
        return await use_case.execute(user_login)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return UserRead.model_validate(current_user)
