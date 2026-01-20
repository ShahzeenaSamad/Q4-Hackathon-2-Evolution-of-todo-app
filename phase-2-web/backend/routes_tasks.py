"""
Task Routes - CRUD Operations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional

from db import get_session
from models import Task, TaskCreate, TaskUpdate, TaskRead
from auth import get_current_user

router = APIRouter()


@router.get("", response_model=dict)
async def get_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query("all", regex="^(all|pending|completed)$"),
    sort: str = Query("created", regex="^(created|title|updated)$"),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Get all tasks for the authenticated user
    """
    # Build query
    query = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Apply sorting
    if sort == "created":
        query = query.order_by(Task.created_at.desc())
    elif sort == "title":
        query = query.order_by(Task.title)
    elif sort == "updated":
        query = query.order_by(Task.updated_at.desc())

    # Get total count
    total_query = select(Task).where(Task.user_id == user_id)
    if status == "pending":
        total_query = total_query.where(Task.completed == False)
    elif status == "completed":
        total_query = total_query.where(Task.completed == True)

    total = len(session.exec(total_query).all())

    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    tasks = session.exec(query).all()

    return {
        "success": True,
        "data": {
            "tasks": tasks,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": (total + limit - 1) // limit
            }
        }
    }


@router.post("", response_model=dict, status_code=201)
async def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Create a new task
    """
    # Validate title
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Title is required"
            }
        })

    if len(task_data.title) > 200:
        raise HTTPException(status_code=400, detail={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Title must be 200 characters or less"
            }
        })

    if task_data.description and len(task_data.description) > 1000:
        raise HTTPException(status_code=400, detail={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Description must be 1000 characters or less"
            }
        })

    # Create task
    task = Task(
        user_id=user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task
    }


@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Get a specific task by ID
    """
    # Get task (user can only see their own tasks)
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        })

    return {
        "success": True,
        "data": task
    }


@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Update a task
    """
    # Get task
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        })

    # Update fields
    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(status_code=400, detail={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Title cannot be empty"
                }
            })
        if len(task_data.title) > 200:
            raise HTTPException(status_code=400, detail={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Title must be 200 characters or less"
                }
            })
        task.title = task_data.title.strip()

    if task_data.description is not None:
        if len(task_data.description) > 1000:
            raise HTTPException(status_code=400, detail={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Description must be 1000 characters or less"
                }
            })
        task.description = task_data.description.strip() if task_data.description else None

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task
    }


@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Delete a task
    """
    # Get task
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        })

    # Delete task
    session.delete(task)
    session.commit()

    return {
        "success": True,
        "data": {
            "message": "Task deleted successfully"
        }
    }


@router.patch("/{task_id}/complete", response_model=dict)
async def toggle_task_completion(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Toggle task completion status
    """
    # Get task
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        })

    # Toggle completion
    task.completed = not task.completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task
    }
