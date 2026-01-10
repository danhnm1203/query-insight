"""SQLAlchemy database models."""
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.domain.entities import (
    DatabaseType,
    MetricType,
    PlanTier,
    QueryStatus,
    RecommendationType,
    RecommendationStatus,
)

Base = declarative_base()


class UserModel(Base):
    """User database model."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    plan_tier = Column(Enum(PlanTier), default=PlanTier.FREE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    databases = relationship("DatabaseModel", back_populates="user", cascade="all, delete-orphan")


class DatabaseModel(Base):
    """Database connection model."""

    __tablename__ = "databases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum(DatabaseType), nullable=False)
    encrypted_connection_string = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_connected_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("UserModel", back_populates="databases")
    queries = relationship("QueryModel", back_populates="database", cascade="all, delete-orphan")
    metrics = relationship("MetricModel", back_populates="database", cascade="all, delete-orphan")


class QueryModel(Base):
    """Query execution model."""

    __tablename__ = "queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    database_id = Column(UUID(as_uuid=True), ForeignKey("databases.id", ondelete="CASCADE"), nullable=False)
    sql_text = Column(Text, nullable=False)
    normalized_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Float, nullable=False)
    explain_plan = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    status = Column(Enum(QueryStatus), default=QueryStatus.SLOW, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    database = relationship("DatabaseModel", back_populates="queries")
    recommendations = relationship("RecommendationModel", back_populates="query", cascade="all, delete-orphan")


class MetricModel(Base):
    """Performance metrics model (TimescaleDB hypertable)."""

    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    database_id = Column(UUID(as_uuid=True), ForeignKey("databases.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    metric_type = Column(Enum(MetricType), nullable=False)
    value = Column(Float, nullable=False)
    extra_data = Column(JSONB, default=dict, nullable=True)

    # Relationships
    database = relationship("DatabaseModel", back_populates="metrics")


class RecommendationModel(Base):
    """Query optimization recommendation model."""

    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("queries.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(RecommendationType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    sql_suggestion = Column(Text, nullable=True)
    estimated_impact = Column(Float, default=0.0, nullable=False)
    confidence = Column(Float, default=0.0, nullable=False)
    status = Column(Enum(RecommendationStatus), default=RecommendationStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    applied_at = Column(DateTime, nullable=True)

    # Relationships
    query = relationship("QueryModel", back_populates="recommendations")
