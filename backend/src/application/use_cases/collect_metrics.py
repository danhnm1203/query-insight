"""Use case for collecting metrics and slow queries from a database."""
import logging
from datetime import datetime
from typing import List
from uuid import UUID

from src.application.interfaces.unit_of_work import IUnitOfWork
from src.infrastructure.services.sql_normalizer import SqlNormalizer
from src.infrastructure.collectors.postgres_collector import PostgresCollector
from src.domain.entities.query import Query
from src.domain.entities.metric import Metric, MetricType

logger = logging.getLogger(__name__)

class CollectMetricsUseCase:
    """UseCase for collecting performance data from a target database."""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, database_id: UUID) -> List[UUID]:
        """
        Collect results from pg_stat_statements and basic metrics.
        
        Args:
            database_id: ID of the database to collect from.
        
        Returns:
            List of new slow query IDs.
        """
        async with self.uow:
            # 1. Get database connection info
            database = await self.uow.databases.get_by_id(database_id)
            if not database or not database.is_active:
                logger.warning(f"Database {database_id} not found or inactive.")
                return []

            # 2. Initialize collector
            collector = PostgresCollector(database.encrypted_connection_string)

            try:
                # 3. Set status to SYNCING
                database.set_syncing()
                await self.uow.databases.save(database)
                await self.uow.commit() # Commit SYNCING status immediately

                # 4. Collect slow queries
                slow_queries_data = await collector.collect_slow_queries(threshold_ms=10.0, limit=20)
                
                queries_to_save = []
                for q_data in slow_queries_data:
                    # Generate a consistent fingerprint
                    normalized_sql = SqlNormalizer.normalize(q_data["sql_text"])
                    
                    query = Query(
                        database_id=database_id,
                        sql_text=q_data["sql_text"],
                        normalized_sql=normalized_sql, 
                        execution_time_ms=q_data["mean_exec_time_ms"],
                        timestamp=datetime.utcnow()
                    )
                    queries_to_save.append(query)
                
                new_query_ids = []
                if queries_to_save:
                    saved_queries = await self.uow.queries.save_all(queries_to_save)
                    new_query_ids = [q.id for q in saved_queries]
                    logger.info(f"Collected {len(queries_to_save)} queries for DB {database_id}")

                # 5. Collect enhanced metrics
                timestamp = datetime.utcnow()
                metrics_to_save = []
                
                # QPS metric (query count)
                metrics_to_save.append(Metric(
                    database_id=database_id,
                    metric_type=MetricType.QPS,
                    value=float(len(slow_queries_data)),
                    timestamp=timestamp,
                    metadata={"captured_queries": len(slow_queries_data)}
                ))
                
                # Average execution time
                if slow_queries_data:
                    avg_exec_time = sum(q["mean_exec_time_ms"] for q in slow_queries_data) / len(slow_queries_data)
                    metrics_to_save.append(Metric(
                        database_id=database_id,
                        metric_type=MetricType.AVG_EXEC_TIME,
                        value=avg_exec_time,
                        timestamp=timestamp,
                        metadata={"query_count": len(slow_queries_data)}
                    ))
                
                # Save all metrics
                for metric in metrics_to_save:
                    await self.uow.metrics.save(metric)
                
                logger.info(f"Saved {len(metrics_to_save)} metrics for DB {database_id}")
                
                # 6. Update last collection timestamps and status
                database.update_last_connected()
                database.update_last_collection()
                database.set_online()
                await self.uow.databases.save(database)

                await self.uow.commit()
                return new_query_ids

            except Exception as e:
                logger.error(f"Error collecting from database {database_id}: {e}")
                
                # Update status to OFFLINE if it wasn't a business logic error
                # Re-fetch database to avoid session issues
                async with self.uow:
                    try:
                        db = await self.uow.databases.get_by_id(database_id)
                        if db:
                            db.set_offline(str(e))
                            await self.uow.databases.save(db)
                            await self.uow.commit()
                    except Exception as inner_e:
                        logger.error(f"Failed to set offline status: {inner_e}")

                raise
