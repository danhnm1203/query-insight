"""SQLAlchemy implementation of Unit of Work."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.unit_of_work import IUnitOfWork
from src.infrastructure.database.repositories.user_repository import PostgresUserRepository
from src.infrastructure.database.repositories.database_repository import PostgresDatabaseRepository
from src.infrastructure.database.repositories.query_repository import PostgresQueryRepository
from src.infrastructure.database.repositories.metric_repository import PostgresMetricRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    """SQLAlchemy implementation of IUnitOfWork."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self.users = PostgresUserRepository(session)
        self.databases = PostgresDatabaseRepository(session)
        self.queries = PostgresQueryRepository(session)
        self.metrics = PostgresMetricRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self):
        """Commit the transaction."""
        await self._session.commit()

    async def rollback(self):
        """Rollback the transaction."""
        await self._session.rollback()
