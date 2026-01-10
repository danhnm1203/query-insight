"""User DTOs for data transfer between layers."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.domain.entities.user import PlanTier


class UserBase(BaseModel):
    """Base user DTO."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """DTO for creating a new user."""
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """DTO for user login."""
    email: EmailStr
    password: str


class UserRead(UserBase):
    """DTO for reading user information."""
    id: UUID
    plan_tier: PlanTier
    is_active: bool
    onboarding_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """DTO for authentication token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """DTO for token payload."""
    email: Optional[str] = None
    user_id: Optional[str] = None
