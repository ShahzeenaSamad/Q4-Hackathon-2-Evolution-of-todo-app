"""
FastAPI Application Entry Point
AI-Powered Todo Chatbot (Phase 3)
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    import time
    logger.info("Starting AI-Powered Todo Chatbot API...")

    # Record startup time for health check uptime calculation
    app.state.start_time = time.time()

    yield
    logger.info("Shutting down AI-Powered Todo Chatbot API...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="AI-Powered Todo Chatbot",
    description="Stateless chat API for AI-powered todo task management using OpenAI GPT-4o",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend communication
# Temporary: Allow all origins for production deployment
# TODO: Lock this down to specific origins in production
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS enabled for origins: {cors_origins}")


@app.get("/health")
def health_check():
    """
    Health check endpoint for liveness probe.

    Returns service status and uptime.
    Used by Kubernetes to check if container needs restart.
    """
    import time
    start_time = getattr(app.state, "start_time", time.time())
    return {
        "status": "healthy",
        "service": "ai-chatbot",
        "version": "1.0.0",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        "uptime": time.time() - start_time
    }


@app.get("/ready")
def readiness_check():
    """
    Readiness check endpoint for deployment monitoring.

    Returns service status and database connectivity.
    Used by Kubernetes to check if container is ready to serve traffic.
    """
    from datetime import datetime
    import time

    # Check database connectivity
    db_status = "connected"
    try:
        # Try to get database session
        from db import get_db
        db = next(get_db())
        db.close()
    except Exception as e:
        db_status = "disconnected"
        logger.error(f"Database check failed: {e}")

    return {
        "status": "ready" if db_status == "connected" else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": {
            "database": db_status
        }
    }


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Powered Todo Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Import and include chat routes
from routes import chat
app.include_router(chat.router)

# Import and include auth routes
from routes import auth
app.include_router(auth.router)

# Import and include tasks routes
from routes import tasks
app.include_router(tasks.router)

logger.info("FastAPI application initialized")
