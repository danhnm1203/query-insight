from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

from src.domain.entities.recommendation import RecommendationType, RecommendationStatus

class RecommendationRead(BaseModel):
    id: UUID
    query_id: UUID
    type: RecommendationType
    title: str
    description: str
    sql_suggestion: Optional[str] = None
    estimated_impact: float
    confidence: float
    status: RecommendationStatus
    created_at: datetime
    applied_at: Optional[datetime] = None

    class Config:
        from_attributes = True
