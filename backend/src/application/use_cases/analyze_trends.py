"""Use case for identifying performance trends and regressions."""
import logging
from uuid import UUID
from typing import List, Dict, Any
from datetime import datetime, timedelta

from src.application.interfaces.unit_of_work import IUnitOfWork

logger = logging.getLogger(__name__)

class AnalyzeTrendsUseCase:
    """Detects queries that are getting slower over time."""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, database_id: UUID) -> List[Dict[str, Any]]:
        """
        Compare recent query performance against a 7-day baseline.
        
        Returns:
            List of detected regressions/trends.
        """
        async with self.uow:
            # 1. Get recent metrics (last 24 hours)
            recent_metrics = await self.uow.queries.get_aggregated_metrics(database_id, hours=24)
            if not recent_metrics:
                return []

            # 2. Get baseline metrics (last 7 days, excluding the last 24 hours would be better, 
            # but for simplicity we'll just take the 7-day average)
            baseline_metrics = await self.uow.queries.get_aggregated_metrics(database_id, hours=168) # 7 days
            
            # Index baseline by normalized_sql for fast lookup
            baseline_map = {m["normalized_sql"]: m for m in baseline_metrics}
            
            regressions = []
            
            # 3. Compare and detect degradation
            for recent in recent_metrics:
                fingerprint = recent["normalized_sql"]
                baseline = baseline_map.get(fingerprint)
                
                if not baseline or baseline["count"] < 5:
                    # Not enough data for a reliable baseline
                    continue
                
                recent_avg = recent["avg_exec_time_ms"]
                baseline_avg = baseline["avg_exec_time_ms"]
                
                # Check for significant degradation (e.g., > 30% increase AND > 50ms absolute increase)
                if recent_avg > baseline_avg * 1.3 and (recent_avg - baseline_avg) > 50:
                    regressions.append({
                        "normalized_sql": fingerprint,
                        "recent_avg_ms": recent_avg,
                        "baseline_avg_ms": baseline_avg,
                        "increase_percentage": ((recent_avg / baseline_avg) - 1) * 100,
                        "count": recent["count"],
                        "last_seen": recent["last_seen"]
                    })
            
            # Sort by absolute increase to show most impactful first
            regressions.sort(key=lambda x: (x["recent_avg_ms"] - x["baseline_avg_ms"]), reverse=True)
            
            return regressions
