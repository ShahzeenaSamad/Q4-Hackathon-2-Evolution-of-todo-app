"""
FastAPI Backend for Todo Web Application
Main entry point with CORS middleware and versioned API router
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan event handler for startup and shutdown events
    """
    # Startup
    logger.info("Starting up FastAPI application...")
    # Initialize database connection check
    from db import check_db_connection
    if check_db_connection():
        logger.info("Database connection successful")
    else:
        logger.warning("Database connection failed - health check will report disconnected")
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application...")
    from db import close_db_connections
    close_db_connections()


# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="FastAPI backend for Todo Web Application with JWT authentication",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Configure CORS middleware
# Read allowed origins from environment or use defaults
import os
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001")
allowed_origins = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router (versioned)
from fastapi import APIRouter, Depends
from routes.auth import router as auth_router
from routes.tasks import router as tasks_router
from auth.middleware import require_auth
api_v1_router = APIRouter(prefix="/api/v1")


# Health check endpoint (T012)
@api_v1_router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API and database connectivity
    Returns:
        JSON response with API status and database connection status
    """
    from db import check_db_connection
    db_connected = check_db_connection()
    return {
        "status": "healthy",
        "database": "connected" if db_connected else "disconnected",
        "version": "1.0.0"
    }


# Include authentication routes (T033) - directly in app
app.include_router(auth_router, prefix="/api/v1/auth")

# Include task routes (each route handles its own auth via verify_jwt)
app.include_router(tasks_router, prefix="/api/v1/tasks")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Todo API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/v1/health"
    }


# Include API router
app.include_router(api_v1_router)


# Run server with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )
