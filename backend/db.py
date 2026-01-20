"""
Database connection and session management for PostgreSQL (Neon)
Uses SQLModel with async support and connection pooling
"""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import Generator, AsyncGenerator
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Please set it in your .env file or environment."
    )

# Convert to async URL if needed for PostgreSQL + asyncpg
# For synchronous operations (current implementation), use psycopg2-binary
# For async operations (future enhancement), use:postgresql+asyncpg://
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create synchronous engine (for current implementation)
engine = create_engine(
    DATABASE_URL,
    echo=bool(os.getenv("PYTHON_ENV") == "development"),  # Log SQL in development
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Additional connections when pool is full
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create async engine (for future async operations)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=bool(os.getenv("PYTHON_ENV") == "development"),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
)

# Create session factories
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
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
    Dependency function to get async database session
    Usage in async FastAPI endpoints:
        db: AsyncSession = Depends(get_async_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def init_db():
    """
    Initialize database tables
    Creates all tables that don't exist yet
    """
    try:
        logger.info("Initializing database...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def init_async_db():
    """
    Initialize database tables asynchronously
    """
    try:
        logger.info("Initializing async database...")
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Async database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing async database: {e}")
        raise


def check_db_connection() -> bool:
    """
    Check if database connection is working
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        db = SessionLocal()
        # Simple query to test connection
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


async def check_async_db_connection() -> bool:
    """
    Check if async database connection is working
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Async database connection check failed: {e}")
        return False


def close_db_connections():
    """
    Close all database connections
    Called on application shutdown
    """
    try:
        logger.info("Closing database connections...")
        engine.dispose()
        async_engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


# Export commonly used items
__all__ = [
    "engine",
    "async_engine",
    "SessionLocal",
    "AsyncSessionLocal",
    "get_db",
    "get_async_db",
    "init_db",
    "init_async_db",
    "check_db_connection",
    "check_async_db_connection",
    "close_db_connections",
]
