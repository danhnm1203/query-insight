"""Metric entity for time-series data."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class MetricType(str, Enum):
    """Types of metrics collected."""
    QPS = "qps"  # Queries per second
    AVG_EXEC_TIME = "avg_exec_time"  # Average execution time
    CONN_COUNT = "conn_count"  # Active connections
    CACHE_HIT_RATIO = "cache_hit_ratio"  # Cache hit ratio
    TPS = "tps"  # Transactions per second
    DEADLOCKS = "deadlocks"  # Deadlock count
    LOCK_WAIT_TIME = "lock_wait_time"  # Lock wait time
    DISK_IO = "disk_io"  # Disk I/O operations


class Metric:
    """Metric entity for storing time-series performance data."""
    
    def __init__(
        self,
        database_id: UUID,
        metric_type: MetricType,
        value: float,
        timestamp: datetime,
        metric_id: Optional[UUID] = None,
        metadata: Optional[dict] = None,
    ):
        self.id = metric_id or uuid4()
        self.database_id = database_id
        self.metric_type = metric_type
        self.value = value
        self.timestamp = timestamp
        self.metadata = metadata or {}
    
    def __repr__(self) -> str:
        return f"<Metric {self.metric_type}: {self.value} at {self.timestamp}>"
