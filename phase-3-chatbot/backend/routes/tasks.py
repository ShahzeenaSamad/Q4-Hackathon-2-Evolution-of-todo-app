"""
Tasks Routes - CRUD operations for task management
Provides REST API for task operations
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from logging import Logger
from datetime import datetime
import uuid

from db import get_db
from models.task import Task, TaskCreate, TaskUpdate
from auth.middleware import verify_jwt

logger = Logger(__name__)

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.get("/")
async def get_all_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max records to return"),
    user_id: str = Depends(verify_jwt),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the authenticated user.

    Returns paginated list of tasks sorted by creation date (newest first).
    """
    try:
        # Get tasks owned by this user
        tasks = (
            db.query(Task)
            .filter(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")

        # Return in format expected by frontend
        return {"data": tasks}
    except Exception as e:
        logger.error(f"Error fetching tasks for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch tasks")


@router.get("/{task_id}")
async def get_task(
    task_id: str,
    user_id: str = Depends(verify_jwt),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.
    """
    try:
        task = db.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Verify ownership
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        logger.info(f"Retrieved task {task_id} for user {user_id}")
        return {"data": task}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch task")


@router.post("/")
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(verify_jwt),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.
    """
    try:
        # Create new task with user_id
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            category=task_data.category,
            completed=False
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        logger.info(f"Created task {task.id} for user {user_id}")
        return {"data": task}
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating task for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create task")


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(verify_jwt),
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    """
    try:
        task = db.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Verify ownership
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        # Update fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.due_date is not None:
            task.due_date = task_data.due_date
        if task_data.category is not None:
            task.category = task_data.category

        task.updated_at = datetime.now()

        db.commit()
        db.refresh(task)

        logger.info(f"Updated task {task_id} for user {user_id}")
        return {"data": task}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update task")


@router.patch("/{task_id}/complete")
async def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(verify_jwt),
    db: Session = Depends(get_db)
):
    """
    Toggle task completion status.
    """
    try:
        task = db.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Verify ownership
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        # Toggle completion
        task.completed = not task.completed
        task.updated_at = datetime.now()

        db.commit()
        db.refresh(task)

        logger.info(f"Toggled task {task_id} completion to {task.completed} for user {user_id}")
        return {"data": task}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error toggling task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to toggle task")


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    user_id: str = Depends(verify_jwt),
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    """
    try:
        task = db.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Verify ownership
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        db.delete(task)
        db.commit()

        logger.info(f"Deleted task {task_id} for user {user_id}")
        return {"data": {"message": "Task deleted successfully"}}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete task")
