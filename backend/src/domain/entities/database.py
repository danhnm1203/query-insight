"""Database entity for QueryInsight."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class DatabaseType(str, Enum):
    """Supported database types."""
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"


class Database:
    """Database entity representing a connected database."""
    
    def __init__(
        self,
        user_id: UUID,
        name: str,
        db_type: DatabaseType,
        encrypted_connection_string: str,
        is_active: bool = True,
        database_id: Optional[UUID] = None,
    ):
        self.id = database_id or uuid4()
        self.user_id = user_id
        self.name = name
        self.type = db_type
        self.encrypted_connection_string = encrypted_connection_string
        self.is_active = is_active
        self.created_at = datetime.utcnow()
        self.last_connected_at: Optional[datetime] = None
    
    def activate(self) -> None:
        """Activate the database connection."""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivate the database connection."""
        self.is_active = False
    
    def update_last_connected(self) -> None:
        """Update the last connected timestamp."""
        self.last_connected_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"<Database {self.name} ({self.type})>"
