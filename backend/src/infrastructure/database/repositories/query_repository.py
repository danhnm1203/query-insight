"""SQLAlchemy implementation of query repository."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.query_repository import IQueryRepository
from src.domain.entities.query import Query, QueryStatus
from src.infrastructure.database.models import QueryModel


from sqlalchemy.orm import selectinload

class PostgresQueryRepository(IQueryRepository):
    """PostgreSQL implementation of IQueryRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, query_id: UUID) -> Optional[Query]:
        """Get query by ID with recommendations."""
        result = await self.session.execute(
            select(QueryModel)
            .options(selectinload(QueryModel.recommendations))
            .where(QueryModel.id == query_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_database_id(self, db_id: UUID, limit: int = 50) -> List[Query]:
        """Get latest queries for a specific database."""
        result = await self.session.execute(
            select(QueryModel)
            .options(selectinload(QueryModel.recommendations))
            .where(QueryModel.database_id == db_id)
            .order_by(desc(QueryModel.timestamp))
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def save(self, query: Query) -> Query:
        """Save a new query or update an existing one."""
        model = await self.session.get(QueryModel, query.id)
        
        if model:
            model.explain_plan = query.explain_plan
            model.status = query.status
        else:
            model = QueryModel(
                id=query.id,
                database_id=query.database_id,
                sql_text=query.sql_text,
                normalized_sql=query.normalized_sql,
                execution_time_ms=query.execution_time_ms,
                explain_plan=query.explain_plan,
                timestamp=query.timestamp,
                status=query.status,
                created_at=datetime.utcnow()
            )
            self.session.add(model)
        
        await self.session.flush()
        return query

    async def save_all(self, queries: List[Query]) -> List[Query]:
        """Save multiple queries."""
        for query in queries:
            await self.save(query)
        return queries

    def _to_entity(self, model: QueryModel) -> Query:
        """Convert QueryModel to Query entity."""
        from src.domain.entities.recommendation import Recommendation
        
        q = Query(
            database_id=model.database_id,
            sql_text=model.sql_text,
            normalized_sql=model.normalized_sql,
            execution_time_ms=model.execution_time_ms,
            explain_plan=model.explain_plan,
            timestamp=model.timestamp,
            query_id=model.id
        )
        q.status = model.status
        
        # Map recommendations if they were loaded
        if hasattr(model, 'recommendations') and model.recommendations:
            q.recommendations = [
                Recommendation(
                    recommendation_id=r.id,
                    query_id=r.query_id,
                    rec_type=r.type,
                    title=r.title,
                    description=r.description,
                    sql_suggestion=r.sql_suggestion,
                    estimated_impact=r.estimated_impact,
                    confidence=r.confidence,
                    status=r.status
                ) for r in model.recommendations
            ]
            
        return q
from datetime import datetime
