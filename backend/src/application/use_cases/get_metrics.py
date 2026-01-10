from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from src.application.dto.metric_dto import MetricRead, MetricsResponse
from src.application.interfaces.repositories.metric_repository import IMetricRepository

class GetMetricsUseCase:
    def __init__(self, metric_repo: IMetricRepository):
        self._metric_repo = metric_repo

    async def execute(self, db_id: UUID, hours: int = 1) -> MetricsResponse:
        """Get metrics for a database for the last X hours."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        metrics = await self._metric_repo.get_by_database_id(db_id, start_time, end_time)
        
        return MetricsResponse(
            database_id=db_id,
            metrics=[MetricRead.from_orm(m) for m in metrics]
        )
