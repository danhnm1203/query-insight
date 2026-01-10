from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.infrastructure.database.session import get_db_session
from src.config import get_settings

router = APIRouter(tags=["monitoring"])
settings = get_settings()

@router.get("/health")
async def health_check(
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Enhanced health check endpoint.
    Checks connectivity to:
    - PostgreSQL Database
    - Redis (via direct connection)
    """
    health_status = {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.env,
        "components": {
            "database": "unknown",
            "redis": "unknown"
        }
    }
    
    status_code = status.HTTP_200_OK

    # Check Database
    try:
        await db.execute(text("SELECT 1"))
        health_status["components"]["database"] = "up"
    except Exception as e:
        health_status["components"]["database"] = "down"
        health_status["status"] = "degraded"
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
    # Check Redis
    try:
        redis = Redis.from_url(settings.redis_url, socket_connect_timeout=1)
        await redis.ping()
        await redis.close()
        health_status["components"]["redis"] = "up"
    except Exception as e:
        health_status["components"]["redis"] = "down"
        health_status["status"] = "degraded"
        # We might not want to fail the whole service if Redis is down, but let's signal degradation
        # status_code = status.HTTP_503_SERVICE_UNAVAILABLE 

    response.status_code = status_code
    return health_status
