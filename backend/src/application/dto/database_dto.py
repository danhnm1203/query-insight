"""Database DTOs for data transfer between layers."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities.database import DatabaseType


class DatabaseBase(BaseModel):
    """Base database DTO."""
    name: str = Field(..., min_length=1, max_length=255)
    type: DatabaseType = DatabaseType.POSTGRES


class DatabaseCreate(DatabaseBase):
    """DTO for connecting a new database."""
    connection_string: str


class DatabaseUpdate(BaseModel):
    """DTO for updating database info."""
    name: Optional[str] = None
    is_active: Optional[bool] = None


class DatabaseRead(DatabaseBase):
    """DTO for reading database information."""
    id: UUID
    user_id: UUID
    is_active: bool
    created_at: datetime
    last_connected_at: Optional[datetime] = None
    last_collection_at: Optional[datetime] = None

    class Config:
        from_attributes = True
