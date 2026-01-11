"""Celery tasks for query collection and analysis."""
import asyncio
from typing import List
from uuid import UUID

from celery import shared_task
from celery.utils.log import get_task_logger

from src.infrastructure.queue.app import celery_app
from src.infrastructure.database.session import AsyncSessionLocal
from src.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from src.application.use_cases.collect_metrics import CollectMetricsUseCase
from src.application.use_cases.analyze_query import AnalyzeQueryUseCase
from src.infrastructure.database.repositories.recommendation_repository import PostgresRecommendationRepository

logger = get_task_logger(__name__)

def run_async(coro):
    """Utility to run async code in a synchronous Celery task."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # This shouldn't normally happen in a worker process unless using gevent/eventlet
        new_loop = asyncio.new_event_loop()
        return new_loop.run_until_complete(coro)
    return loop.run_until_complete(coro)

@celery_app.task(name="src.infrastructure.queue.tasks.collect_database_metrics")
def collect_database_metrics(database_id: str):
    """Task to collect metrics for a single database."""
    logger.info(f"Starting metrics collection for database: {database_id}")
    
    async def _collect():
        async with AsyncSessionLocal() as session:
            uow = SqlAlchemyUnitOfWork(session)
            use_case = CollectMetricsUseCase(uow)
            new_query_ids = await use_case.execute(UUID(database_id))
            
            # Dispatch analysis tasks for each new slow query
            for q_id in new_query_ids:
                analyze_query.delay(str(q_id))
            
    try:
        run_async(_collect())
        logger.info(f"Successfully collected metrics for database: {database_id}")
    except Exception as e:
        logger.error(f"Failed to collect metrics for database {database_id}: {e}")
        raise

@celery_app.task(name="src.infrastructure.queue.tasks.collect_all_databases_metrics")
def collect_all_databases_metrics():
    """Task to trigger metrics collection for all active databases."""
    logger.info("Triggering metrics collection for all active databases")
    
    async def _trigger():
        async with AsyncSessionLocal() as session:
            uow = SqlAlchemyUnitOfWork(session)
            active_dbs = await uow.databases.get_all_active()
            
            for db in active_dbs:
                # Dispatch individual tasks for each database
                collect_database_metrics.delay(str(db.id))
            
            return len(active_dbs)
            
    try:
        count = run_async(_trigger())
        logger.info(f"Triggered collection for {count} databases")
    except Exception as e:
        logger.error(f"Failed to trigger bulk metrics collection: {e}")
        raise

@celery_app.task(name="src.infrastructure.queue.tasks.analyze_query")
def analyze_query(query_id: str):
    """Task to analyze a specific slow query and generate recommendations."""
    logger.info(f"Starting analysis for query: {query_id}")
    
    async def _analyze():
        async with AsyncSessionLocal() as session:
            uow = SqlAlchemyUnitOfWork(session)
            # We need the recommendation repo which might not be in UOW yet
            # Check UOW implementation or just use session
            rec_repo = PostgresRecommendationRepository(session)
            use_case = AnalyzeQueryUseCase(uow.databases, uow.queries, rec_repo)
            await use_case.execute(UUID(query_id))
            # Commit the session to persist recommendations
            await session.commit()
            
    try:
        run_async(_analyze())
        logger.info(f"Successfully analyzed query: {query_id}")
    except Exception as e:
        logger.error(f"Failed to analyze query {query_id}: {e}")
        raise
