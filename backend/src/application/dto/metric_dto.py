from datetime import datetime
from uuid import UUID
from typing import Dict, Optional, List
from pydantic import BaseModel

from src.domain.entities.metric import MetricType

class MetricRead(BaseModel):
    timestamp: datetime
    metric_type: MetricType
    value: float
    metadata: Optional[Dict] = None

    class Config:
        from_attributes = True

class MetricsResponse(BaseModel):
    database_id: UUID
    metrics: List[MetricRead]
