"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.presentation.api.v1.auth import router as auth_router
from src.presentation.api.v1.databases import router as database_router
from src.presentation.api.v1.metrics import router as metrics_router
from src.presentation.api.v1.queries import router as queries_router
from src.presentation.api.v1.recommendations import router as recommendations_router
from src.presentation.api.v1.intelligence import router as intelligence_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan events."""
    # Startup
    print(f"🚀 Starting {settings.app_name}...")
    print(f"📊 Environment: {settings.env}")
    
    # Initialize Sentry if configured
    if settings.sentry_dsn:
        import sentry_sdk
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.env,
            traces_sample_rate=0.1 if settings.is_production else 1.0,
        )
        print("✅ Sentry monitoring initialized")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Database Query Performance Analyzer - Optimize your queries automatically",
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
        "environment": settings.env,
    }


# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(database_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(queries_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")
app.include_router(intelligence_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": settings.app_name,
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.presentation.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
    )
