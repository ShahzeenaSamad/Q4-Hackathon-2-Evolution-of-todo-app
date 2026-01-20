"""
Database connection and session management for PostgreSQL
Uses SQLModel with connection pooling
"""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import Generator, AsyncGenerator
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Database URL from environment (for Hugging Face Spaces)
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Please set it in Hugging Face Space secrets."
    )

logger.info(f"Database URL configured: {DATABASE_URL[:20]}...")

# Convert to async URL for asyncpg
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create synchronous engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL logging in production
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,  # Smaller pool for Hugging Face
    max_overflow=10,  # Additional connections when pool is full
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

# Create session factories
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

AsyncSessionLocal = sessionmaker(
    engine.class_config(async_engine),
    class_=AsyncSession,
    expire_on_commit=False,
)

def get_db() -> Generator[Session, None, None]:
    """
    Get database session (synchronous)
    Usage in FastAPI endpoints:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session
    Usage in FastAPI endpoints:
        db: AsyncSession = Depends(get_async_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def init_db() -> None:
    """
    Initialize database tables
    Call this on application startup
    """
    from models.user import User
    from models.task import Task
    
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")

async def init_async_db() -> None:
    """
    Initialize database tables (async version)
    """
    from models.user import User
    from models.task import Task
    
    logger.info("Creating database tables (async)...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created successfully (async)")

def check_db_connection() -> bool:
    """
    Check if database connection is working
    Returns True if connection successful, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection check: SUCCESS")
        return True
    except Exception as e:
        logger.error(f"Database connection check: FAILED - {e}")
        return False
