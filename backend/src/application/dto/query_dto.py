from datetime import datetime
from uuid import UUID
from typing import Dict, Optional, List
from pydantic import BaseModel

from src.application.dto.recommendation_dto import RecommendationRead
from src.domain.entities.query import QueryStatus

class QueryRead(BaseModel):
    id: UUID
    database_id: UUID
    sql_text: str
    normalized_sql: str
    execution_time_ms: float
    explain_plan: Optional[Dict] = None
    timestamp: datetime
    status: QueryStatus
    recommendations: List[RecommendationRead] = []

    class Config:
        from_attributes = True
