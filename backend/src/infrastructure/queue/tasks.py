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
            await use_case.execute(UUID(database_id))
            
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
