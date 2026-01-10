"""SQLAlchemy implementation of metric repository."""
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.metric_repository import IMetricRepository
from src.domain.entities.metric import Metric, MetricType
from src.infrastructure.database.models import MetricModel


class PostgresMetricRepository(IMetricRepository):
    """PostgreSQL implementation of IMetricRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_database_id(
        self, db_id: UUID, start_time: datetime, end_time: datetime
    ) -> List[Metric]:
        """Get metrics for a specific database and time range."""
        result = await self.session.execute(
            select(MetricModel).where(
                and_(
                    MetricModel.database_id == db_id,
                    MetricModel.timestamp >= start_time,
                    MetricModel.timestamp <= end_time
                )
            ).order_by(MetricModel.timestamp)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def save(self, metric: Metric) -> Metric:
        """Save a new metric."""
        model = MetricModel(
            timestamp=metric.timestamp,
            database_id=metric.database_id,
            metric_type=metric.metric_type,
            value=metric.value,
            extra_data=metric.metadata
        )
        self.session.add(model)
        await self.session.flush()
        return metric

    async def save_all(self, metrics: List[Metric]) -> List[Metric]:
        """Save multiple metrics."""
        for metric in metrics:
            model = MetricModel(
                timestamp=metric.timestamp,
                database_id=metric.database_id,
                metric_type=metric.metric_type,
                value=metric.value,
                extra_data=metric.metadata
            )
            self.session.add(model)
        await self.session.flush()
        return metrics

    def _to_entity(self, model: MetricModel) -> Metric:
        """Convert MetricModel to Metric entity."""
        return Metric(
            database_id=model.database_id,
            timestamp=model.timestamp,
            metric_type=model.metric_type,
            value=model.value,
            metadata=model.extra_data,
            metric_id=None # Metric model doesn't have a separate ID in the schema (standard for hypertable)
        )
