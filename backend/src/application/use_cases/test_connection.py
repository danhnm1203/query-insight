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
            
        collector = PostgresCollector(connection_string)
        try:
            # Try to connect and run a simple query
            await collector.get_metrics()
            return True
        except Exception:
            return False
