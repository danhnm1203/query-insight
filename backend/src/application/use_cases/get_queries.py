from typing import List
from uuid import UUID

from src.application.dto.query_dto import QueryRead
from src.application.interfaces.repositories.query_repository import IQueryRepository

class GetSlowQueriesUseCase:
    def __init__(self, query_repo: IQueryRepository):
        self._query_repo = query_repo

    async def execute(self, db_id: UUID, limit: int = 50) -> List[QueryRead]:
        """Get the latest slow queries for a database."""
        queries = await self._query_repo.get_by_database_id(db_id, limit)
        
        return [QueryRead.from_orm(q) for q in queries]

class GetQueryDetailsUseCase:
    def __init__(self, query_repo: IQueryRepository):
        self._query_repo = query_repo

    async def execute(self, query_id: UUID) -> QueryRead:
        """Get details for a specific query."""
        query = await self._query_repo.get_by_id(query_id)
        if not query:
            return None
        return QueryRead.from_orm(query)
