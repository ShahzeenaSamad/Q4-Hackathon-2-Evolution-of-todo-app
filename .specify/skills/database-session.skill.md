# Database Session Management Skill

## Description
Reusable skill for managing database sessions with proper error handling, transaction management, and cleanup.

## When to Use
- Any database operation requiring a session
- Batch database operations
- Transactions that need rollback capability
- Testing with database fixtures

## Capabilities

### 1. Get Session
```python
from db import SessionLocal

def get_db_session():
    """Get a new database session with proper error handling"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

### 2. Execute with Transaction
```python
def execute_in_transaction(session, operation, *args, **kwargs):
    """Execute operation with automatic transaction management"""
    try:
        result = operation(session, *args, **kwargs)
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise e
```

### 3. Query with Pagination
```python
def execute_paginated_query(session, statement, page=1, page_size=50):
    """Execute query with pagination support"""
    offset = (page - 1) * page_size
    statement = statement.offset(offset).limit(page_size)
    return session.execute(statement).scalars().all()
```

## Error Handling Patterns

### Always Use Context Managers
```python
# GOOD
with SessionLocal() as session:
    result = session.execute(statement)

# BAD
session = SessionLocal()
result = session.execute(statement)
session.close()  # Can be missed on error
```

### Rollback on Errors
```python
try:
    session.add(item)
    session.commit()
except Exception as e:
    session.rollback()
    logger.error(f"Transaction failed: {e}")
    raise
```

## Usage Examples

### Query Example
```python
from db import SessionLocal
from sqlmodel import select

def get_user_tasks(user_id: str):
    with SessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.execute(statement).scalars().all()
        return tasks
```

### Insert Example
```python
def create_task(user_id: str, title: str):
    with SessionLocal() as session:
        task = Task(user_id=user_id, title=title)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
```

## Best Practices
1. Always use `with` statements for session management
2. Commit only after all operations succeed
3. Rollback on any exception
4. Close sessions in `finally` blocks
5. Use `session.refresh()` after INSERT to get DB-generated values

## Dependencies
- SQLModel Session from db.py
- Exception handling from Python standard lib
