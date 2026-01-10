"""Celery application configuration."""
from celery import Celery
from src.config import get_settings

settings = get_settings()

celery_app = Celery(
    "query_insight",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["src.infrastructure.queue.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Short visibility timeout for quick retries
    broker_transport_options={'visibility_timeout': 3600},
)

# Optional: Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "collect-all-metrics": {
        "task": "src.infrastructure.queue.tasks.collect_all_databases_metrics",
        "schedule": 300.0, # Every 5 minutes
    },
}
