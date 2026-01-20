"""
Task Service - Task CRUD operations
"""
from sqlmodel import Session, select
from models.task import Task
from typing import List, Optional
from datetime import datetime


def get_user_tasks(user_id: str, session: Session) -> List[Task]:
    """Get all tasks for a specific user"""
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    results = session.execute(statement)
    return list(results.scalars().all())


def get_task_by_id(task_id: int, user_id: str, session: Session) -> Optional[Task]:
    """Get a specific task by ID (ensures user owns the task)"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    results = session.execute(statement)
    return results.scalar_one_or_none()


def create_task(title: str, user_id: str, description: str = None, session: Session = None) -> Task:
    """Create a new task for a user"""
    task = Task(title=title, user_id=user_id, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(task_id: int, user_id: str, session: Session, **kwargs) -> Optional[Task]:
    """Update an existing task"""
    task = get_task_by_id(task_id, user_id, session)
    if not task:
        return None

    # Update fields
    for key, value in kwargs.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)

    task.updated_at = datetime.now()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(task_id: int, user_id: str, session: Session) -> bool:
    """Delete a task"""
    task = get_task_by_id(task_id, user_id, session)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(task_id: int, user_id: str, session: Session) -> Optional[Task]:
    """Toggle task completion status"""
    task = get_task_by_id(task_id, user_id, session)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.now()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
