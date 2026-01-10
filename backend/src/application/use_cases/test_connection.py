from typing import List
from uuid import UUID
from datetime import datetime

from src.application.dto.database_dto import DatabaseRead
from src.application.interfaces.repositories.database_repository import IDatabaseRepository
from src.infrastructure.collectors.postgres_collector import PostgresCollector

class TestDatabaseConnectionUseCase:
    def __init__(self, db_repo: IDatabaseRepository):
        self._db_repo = db_repo

    async def execute(self, connection_string: str, db_type: str = "postgres") -> bool:
        """
        Test if a connection can be established with the provided connection string.
        """
        if db_type != "postgres":
            # For now only postgres is supported
            return False
            
        # asyncpg expects 'postgresql://' not 'postgresql+asyncpg://'
        clean_connection_string = connection_string.replace("postgresql+asyncpg://", "postgresql://")
            
        collector = PostgresCollector(clean_connection_string)
        try:
            # Try to connect
            await collector.test_connection()
            return True
        except Exception:
            return False
