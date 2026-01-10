"""Use case for collecting metrics and slow queries from a database."""
import logging
from datetime import datetime
from uuid import UUID

from src.application.interfaces.unit_of_work import IUnitOfWork
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
                # 3. Collect slow queries
                slow_queries_data = await collector.collect_slow_queries(threshold_ms=10.0, limit=20)
                
                queries_to_save = []
                for q_data in slow_queries_data:
                    query = Query(
                        database_id=database_id,
                        sql_text=q_data["sql_text"],
                        normalized_sql=q_data["sql_text"], 
                        execution_time_ms=q_data["mean_exec_time_ms"],
                        timestamp=datetime.utcnow()
                    )
                    queries_to_save.append(query)
                
                new_query_ids = []
                if queries_to_save:
                    saved_queries = await self.uow.queries.save_all(queries_to_save)
                    new_query_ids = [q.id for q in saved_queries]
                    logger.info(f"Collected {len(queries_to_save)} queries for DB {database_id}")

                # 4. Collect basic metrics
                metric = Metric(
                    database_id=database_id,
                    metric_type=MetricType.QPS,
                    value=float(len(slow_queries_data)),
                    timestamp=datetime.utcnow(),
                    metadata={"captured_queries": len(slow_queries_data)}
                )
                await self.uow.metrics.save(metric)
                
                # 5. Update last collection timestamps
                database.update_last_connected()
                database.update_last_collection()
                await self.uow.databases.save(database)

                await self.uow.commit()
                return new_query_ids

            except Exception as e:
                logger.error(f"Error collecting from database {database_id}: {e}")
                await self.uow.rollback()
                raise
