# Database Schema Specification

## Database Overview

**Database Provider:** Neon Serverless PostgreSQL
**ORM:** SQLModel (built on SQLAlchemy + Pydantic)
**Migration Tool:** Alembic (if needed)

---

## Database Connection

**Connection String Format:**
```
postgresql://username:password@host/database_name
```

**Environment Variable:**
```bash
DATABASE_URL=postgresql://user:pass@ep-cool-neon-db.us-east-2.aws.neon.tech/neondb
```

**Connection Pooling:**
```python
from sqlmodel import create_engine, Session

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Connection pool size
    max_overflow=20  # Additional connections when needed
)
```

---

## Tables

### Users Table

**Managed By:** Better Auth
**Purpose:** Store user authentication information

**Schema:**
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,              -- UUID (managed by Better Auth)
    email TEXT UNIQUE NOT NULL,       -- User email (unique)
    name TEXT,                        -- Display name (optional)
    emailVerifiedAt TIMESTAMP,        -- Email verification timestamp
    image TEXT,                       -- Profile image URL
    createdAt TIMESTAMP DEFAULT NOW(),
    updatedAt TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
```

**Field Details:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | TEXT | PRIMARY KEY | UUID identifier (managed by Better Auth) |
| `email` | TEXT | UNIQUE, NOT NULL | User's email address |
| `name` | TEXT | NULLABLE | Display name |
| `emailVerifiedAt` | TIMESTAMP | NULLABLE | When email was verified |
| `image` | TEXT | NULLABLE | Profile picture URL |
| `createdAt` | TIMESTAMP | DEFAULT NOW() | Account creation time |
| `updatedAt` | TIMESTAMP | DEFAULT NOW() | Last update time |

**SQLModel Definition:**
```python
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    emailVerifiedAt: Optional[datetime] = None
    image: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
```

---

### Tasks Table

**Managed By:** Our Application
**Purpose:** Store user tasks

**Schema:**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

**Field Details:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-incrementing task ID |
| `user_id` | TEXT | NOT NULL, FK | Foreign key to users table |
| `title` | VARCHAR(200) | NOT NULL | Task title |
| `description` | TEXT | NULLABLE | Task description |
| `completed` | BOOLEAN | DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**SQLModel Definition:**
```python
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional)
    user: Optional["User"] = Relationship(back_populates="tasks")
```

**Indexes Explained:**

1. **idx_tasks_user_id:**
   - Speeds up queries filtering by user
   - Used in almost all queries (data isolation)
   - Essential for performance

2. **idx_tasks_completed:**
   - Speeds up filtering by completion status
   - Used for "pending" vs "completed" views

3. **idx_tasks_created_at:**
   - Speeds up sorting by creation date
   - DESC for most-recent-first sorting

---

## Entity Relationships

### User ↔ Tasks Relationship

**Relationship Type:** One-to-Many

```
┌─────────────┐         ┌─────────────┐
│    User     │         │    Task     │
├─────────────┤         ├─────────────┤
│ id (PK)     │◄────────│ user_id (FK)│
│ email       │         │ id (PK)     │
│ name        │         │ title       │
│ ...         │         │ ...         │
└─────────────┘         └─────────────┘
       │                         ▲
       └─────────────────────────┘
           One user has many tasks
```

**Cascade Delete:**
- When a user is deleted, all their tasks are automatically deleted
- Specified by `ON DELETE CASCADE` in foreign key constraint

---

## Database Models

### SQLModel Classes

**Base Models:**
```python
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class UserBase(SQLModel):
    email: str
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str  # Not stored in User table (hashed)

class UserRead(UserBase):
    id: str
    emailVerifiedAt: Optional[datetime] = None
    image: Optional[str] = None
    createdAt: datetime
```

**Task Models:**
```python
class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass  # Inherits title and description

class TaskUpdate(TaskBase):
    title: Optional[str] = None  # Both optional for update
    description: Optional[str] = None

class TaskRead(TaskBase):
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

---

## Database Operations

### Create Operation

```python
from sqlmodel import Session

def create_task(session: Session, user_id: str, task_data: TaskCreate):
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Read Operation

```python
def get_user_tasks(session: Session, user_id: str, limit: int = 20):
    return session.exec(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .limit(limit)
    ).all()
```

### Update Operation

```python
def update_task(session: Session, task_id: int, user_id: str, task_data: TaskUpdate):
    task = session.exec(
        select(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if task:
        task.title = task_data.title or task.title
        task.description = task_data.description or task.description
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

    return task
```

### Delete Operation

```python
def delete_task(session: Session, task_id: int, user_id: str):
    task = session.exec(
        select(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if task:
        session.delete(task)
        session.commit()

    return task
```

---

## Data Validation

### Title Validation

```python
from pydantic import field_validator

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

### Description Validation

```python
class TaskBase(SQLModel):
    description: Optional[str] = Field(default=None, max_length=1000)

    @field_validator('description')
    def sanitize_description(cls, v):
        if v:
            # Strip HTML tags (basic sanitization)
            import re
            v = re.sub(r'<[^>]+>', '', v)
            v = v.strip()
        return v
```

---

## Migration Strategy

### Initial Setup

**Option 1: Automatic Creation (Development)**
```python
from sqlmodel import SQLModel

# Create all tables
SQLModel.metadata.create_all(engine)
```

**Option 2: Alembic Migrations (Production)**

**Setup:**
```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic
```

**Configure alembic/env.py:**
```python
from sqlmodel import SQLModel
from myapp.models import User, Task

# Add models to metadata
target_metadata = SQLModel.metadata
```

**Create Migration:**
```bash
alembic revision --autogenerate -m "Initial migration"
```

**Run Migration:**
```bash
alembic upgrade head
```

---

## Database Seeding

**Purpose:** Add initial data for testing

```python
def seed_database(session: Session):
    # Create test user
    user = User(
        id="test-user-123",
        email="test@example.com",
        name="Test User"
    )
    session.add(user)

    # Create sample tasks
    tasks = [
        Task(
            user_id=user.id,
            title="Sample Task 1",
            description="This is a sample task",
            completed=False
        ),
        Task(
            user_id=user.id,
            title="Sample Task 2",
            completed=True
        )
    ]
    session.add_all(tasks)
    session.commit()
```

---

## Performance Optimization

### Query Optimization

**Use Indexes:**
```python
# GOOD - Uses index
select(Task).where(Task.user_id == user_id)

# BAD - Full table scan
select(Task).where(Task.title.like("%search%"))
```

**Limit Results:**
```python
# Always use pagination
session.exec(
    select(Task)
    .where(Task.user_id == user_id)
    .limit(20)
    .offset(0)
).all()
```

### Connection Pooling

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,         # Maintain 10 connections
    max_overflow=20,      # Allow 20 additional connections
    pool_recycle=3600,    # Recycle connections after 1 hour
    pool_pre_ping=True    # Verify connections before use
)
```

---

## Backup Strategy

**Neon Serverless Features:**
- ✅ Automatic daily backups
- ✅ Point-in-time recovery (up to 7 days)
- ✅ Branching for development/testing

**Manual Backup:**
```bash
# Using pg_dump
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

---

## Security Considerations

### SQL Injection Prevention

**SQLModel automatically handles parameterized queries:**
```python
# SAFE - Parameters are escaped
user_id = "user_123"
session.exec(select(Task).where(Task.user_id == user_id))

# NEVER DO THIS - SQL injection vulnerability
query = f"SELECT * FROM tasks WHERE user_id = '{user_id}'"
session.exec(query)
```

### Data Isolation

**Always filter by user_id:**
```python
# CORRECT - User's tasks only
def get_tasks(session: Session, user_id: str):
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

# WRONG - Returns all tasks (INSECURE!)
def get_tasks_insecure(session: Session):
    return session.exec(select(Task)).all()
```

---

## Monitoring

### Slow Query Logging

```python
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Database Health Check

```python
@app.get("/api/v1/health")
def health_check(session: Session = Depends(get_session)):
    try:
        session.exec(select(User).limit(1))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected"}
```

---

## Related Specifications

- **Overview:** `@specs/overview.md`
- **Architecture:** `@specs/architecture.md`
- **Features:** `@specs/features/`
- **API:** `@specs/api/rest-endpoints.md`
- **UI:** `@specs/ui/`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
