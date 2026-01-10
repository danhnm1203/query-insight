"""Unit of Work interface."""
from abc import ABC, abstractmethod

from src.application.interfaces.repositories.user_repository import IUserRepository
from src.application.interfaces.repositories.database_repository import IDatabaseRepository
from src.application.interfaces.repositories.query_repository import IQueryRepository
from src.application.interfaces.repositories.metric_repository import IMetricRepository


class IUnitOfWork(ABC):
    """Interface for Unit of Work pattern."""
    
    users: IUserRepository
    databases: IDatabaseRepository
    queries: IQueryRepository
    metrics: IMetricRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        """Commit the changes."""
        pass

    @abstractmethod
    async def rollback(self):
        """Rollback the changes."""
        pass
