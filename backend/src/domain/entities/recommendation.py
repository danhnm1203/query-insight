"""Recommendation entity for query optimization suggestions."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class RecommendationType(str, Enum):
    """Types of recommendations."""
    INDEX = "index"  # Add missing index
    REWRITE = "rewrite"  # Rewrite query for better performance
    PARTITION = "partition"  # Add table partitioning
    MATERIALIZED_VIEW = "materialized_view"  # Create materialized view
    QUERY_CACHE = "query_cache"  # Enable query caching
    DENORMALIZE = "denormalize"  # Denormalize tables
    LIMIT = "limit"  # Add LIMIT clause
    AVOID_N_PLUS_ONE = "avoid_n_plus_one"  # Fix N+1 query pattern
    SCALING = "scaling"  # Scale database resources
    SCHEMA_CHANGE = "schema_change"  # Change table schema (e.g. data type)


class RecommendationStatus(str, Enum):
    """Status of a recommendation."""
    PENDING = "pending"
    APPLIED = "applied"
    DISMISSED = "dismissed"
    TESTING = "testing"


class Recommendation:
    """Recommendation entity for query optimization suggestions."""
    
    def __init__(
        self,
        query_id: UUID,
        rec_type: RecommendationType,
        title: str,
        description: str,
        sql_suggestion: Optional[str] = None,
        estimated_impact: float = 0.0,
        confidence: float = 0.0,
        status: RecommendationStatus = RecommendationStatus.PENDING,
        recommendation_id: Optional[UUID] = None,
    ):
        self.id = recommendation_id or uuid4()
        self.query_id = query_id
        self.type = rec_type
        self.title = title
        self.description = description
        self.sql_suggestion = sql_suggestion
        self.estimated_impact = estimated_impact  # 0-100 percentage improvement
        self.confidence = confidence  # 0-1 confidence score
        self.status = status
        self.created_at = datetime.utcnow()
        self.applied_at: Optional[datetime] = None
    
    def apply(self) -> None:
        """Mark recommendation as applied."""
        self.status = RecommendationStatus.APPLIED
        self.applied_at = datetime.utcnow()
    
    def dismiss(self) -> None:
        """Mark recommendation as dismissed."""
        self.status = RecommendationStatus.DISMISSED
    
    def is_high_impact(self, threshold: float = 50.0) -> bool:
        """Check if recommendation has high potential impact."""
        return self.estimated_impact >= threshold
    
    def __repr__(self) -> str:
        return f"<Recommendation {self.type}: {self.title} ({self.estimated_impact}% impact)>"
