"""
Database Configuration for Phase 3
Extends Phase 2 database configuration
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Please configure it in your .env file."
    )

# Create engine with connection pooling (from Phase 2 configuration)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query debugging
    pool_pre_ping=True,  # Verify connections before using
    pool_size=20,  # Increased for better concurrency
    max_overflow=30,  # Additional connections when pool is full
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Dependency function to get database session.
    Use with FastAPI Depends():
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db():
    """
    Initialize database - create all tables.
    Note: We use Alembic for migrations in production.
    This function is mainly for testing.
    """
    from models import user, task, conversation, message
    SQLModel.metadata.create_all(engine)
