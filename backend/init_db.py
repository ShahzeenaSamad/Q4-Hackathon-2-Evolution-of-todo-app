"""
Database schema initialization for Todo App
Creates users and tasks tables with Better Auth compatibility
Includes indexes and foreign key constraints
"""
from sqlmodel import SQLModel, Field, Relationship, Column, Text, ForeignKey, Boolean, DateTime
from sqlalchemy import Index, UniqueConstraint
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class User(SQLModel, table=True):
    """
    User model compatible with Better Auth
    Matches Better Auth's expected schema
    """
    __tablename__ = "users"

    # Better Auth uses TEXT type for id (UUID)
    id: str = Field(default=None, sa_column=Column(Text, primary_key=True))

    # Email must be unique
    email: str = Field(unique=True, index=True, max_length=255)

    # Password hash (bcrypt)
    password_hash: str = Field(sa_column=Column(Text))

    # Optional name field
    name: Optional[str] = Field(default=None, max_length=255)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")

    # Constraints
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )


class Task(SQLModel, table=True):
    """
    Task model with user isolation
    All tasks are scoped to a specific user
    """
    __tablename__ = "tasks"

    # Auto-incrementing ID
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key to users table (Better Auth uses TEXT for user IDs)
    user_id: str = Field(
        sa_column=Column(Text, ForeignKey("users.id", ondelete="CASCADE"))
    )

    # Task title (required, 1-200 chars)
    title: str = Field(max_length=200)

    # Task description (optional, 0-1000 chars)
    description: Optional[str] = Field(default=None, max_length=1000)

    # Completion status
    completed: bool = Field(default=False, sa_column=Column(Boolean, default=False))

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tasks")

    # Indexes for performance
    __table_args__ = (
        Index("idx_tasks_user_id", "user_id"),
        Index("idx_tasks_completed", "completed"),
        Index("idx_tasks_created_at", "created_at", postgresql_using="btree"),
    )


def create_all_tables():
    """
    Create all database tables with indexes and constraints
    This function should be called during application initialization
    """
    try:
        logger.info("Creating database tables...")

        # Import engine from db module
        from db import engine

        # Create all tables
        SQLModel.metadata.create_all(engine)

        logger.info("Database tables created successfully")
        logger.info("Created tables: users, tasks")
        logger.info("Created indexes: idx_tasks_user_id, idx_tasks_completed, idx_tasks_created_at")
        logger.info("Created constraints: uq_users_email, fk_tasks_user_id (CASCADE)")

    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_all_tables():
    """
    Drop all database tables
    WARNING: This will delete all data!
    Use only for testing/resetting
    """
    try:
        logger.warning("Dropping all database tables...")
        from db import engine

        SQLModel.metadata.drop_all(engine)
        logger.info("All database tables dropped")

    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def reset_database():
    """
    Reset database by dropping and recreating all tables
    WARNING: This will delete all data!
    Use only for testing/resetting
    """
    try:
        logger.warning("Resetting database...")
        drop_all_tables()
        create_all_tables()
        logger.info("Database reset completed")

    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise


if __name__ == "__main__":
    """
    Main entry point for running database initialization
    Usage: python init_db.py
    """
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Check if DATABASE_URL is set
    if not os.getenv("DATABASE_URL"):
        raise ValueError("DATABASE_URL environment variable not set")

    # Create tables
    create_all_tables()

    print("\n" + "="*60)
    print("Database initialization completed successfully!")
    print("="*60)
    print("\nTables created:")
    print("  - users (id, email, password_hash, name, created_at)")
    print("  - tasks (id, user_id, title, description, completed, created_at, updated_at)")
    print("\nIndexes created:")
    print("  - idx_tasks_user_id (for user-scoped queries)")
    print("  - idx_tasks_completed (for filtering by completion status)")
    print("  - idx_tasks_created_at (for reverse chronological ordering)")
    print("\nConstraints created:")
    print("  - uq_users_email (unique email constraint)")
    print("  - fk_tasks_user_id (foreign key with CASCADE delete)")
    print("\n" + "="*60)
