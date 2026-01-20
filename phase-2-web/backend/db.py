"""
Database Connection and Session Management
"""

from sqlmodel import create_engine, Session
from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = getenv("DATABASE_URL", "sqlite:///./test.db")

# Warn if using default SQLite
if DATABASE_URL == "sqlite:///./test.db":
    print("WARNING: Using SQLite test database. Set DATABASE_URL for production.")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development (set to False in production)
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Connection pool size
    max_overflow=20  # Additional connections when needed
)


def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize database tables"""
    from sqlmodel import SQLModel
    from models import User, Task

    SQLModel.metadata.create_all(engine)
    print("SUCCESS: Database tables created successfully!")
