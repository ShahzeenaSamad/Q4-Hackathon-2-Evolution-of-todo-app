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
    logger.info("Starting AI-Powered Todo Chatbot API...")
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
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS enabled for origins: {cors_origins}")


@app.get("/health")
def health_check():
    """
    Health check endpoint for deployment monitoring.

    Returns service status and can be used by load balancers
    to check service availability.
    """
    return {"status": "healthy", "service": "ai-chatbot", "version": "1.0.0"}


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

logger.info("FastAPI application initialized")
