"""
Task Routes - CRUD Operations for Tasks
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import Session
from typing import List
from datetime import datetime

from models.task import Task
from services.task_service import (
    get_user_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion
)
from auth.middleware import verify_jwt
from db import get_db


router = APIRouter()


@router.get("/")
def list_tasks(user_id: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    """
    Get all tasks for the authenticated user.
    Returns tasks ordered by creation date (newest first).
    """
    tasks = get_user_tasks(user_id, db)

    return {
        "success": True,
        "data": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]
    }


@router.post("/")
def create_new_task(task_data: dict, user_id: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    """
    Create a new task for the authenticated user.
    Request body: { "title": "Task title", "description": "Optional description" }
    """
    # Validate title
    title = task_data.get("title", "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    description = task_data.get("description")

    try:
        task = create_task(
            title=title,
            user_id=user_id,
            description=description,
            session=db
        )

        return {
            "success": True,
            "data": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.get("/{task_id}")
def get_task(task_id: int, user_id: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task = get_task_by_id(task_id, user_id, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
    }


@router.put("/{task_id}")
def update_existing_task(task_id: int, task_data: dict, user_id: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    """
    Update an existing task.
    Request body can include: title, description, completed
    """
    # Extract update fields
    update_fields = {}
    if "title" in task_data:
        title = task_data["title"].strip()
        if title:
            update_fields["title"] = title
    if "description" in task_data:
        update_fields["description"] = task_data["description"]
    if "completed" in task_data:
        update_fields["completed"] = task_data["completed"]

    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    task = update_task(task_id, user_id, db, **update_fields)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
    }


@router.patch("/{task_id}/complete")
def toggle_complete(task_id: int, user_id: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    """Toggle task completion status."""
    task = toggle_task_completion(task_id, user_id, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
    }


@router.delete("/{task_id}")
def delete_existing_task(task_id: int, user_id: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    """Delete a task."""
    success = delete_task(task_id, user_id, db)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": {"message": "Task deleted successfully"}
    }
