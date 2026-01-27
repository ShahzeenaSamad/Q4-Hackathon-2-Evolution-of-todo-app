"""
Delete Task MCP Tool
Removes a task from the user's list
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select

from mcp_tools.base import MCPTool, MCPToolResponse
from mcp_tools.exceptions import ValidationError, NotFoundError, OwnershipError
from models import Task


class DeleteTaskTool(MCPTool):
    """
    MCP tool for deleting tasks.

    Allows users to remove tasks by ID or by matching title.
    Handles disambiguation when multiple tasks match.
    """

    @property
    def name(self) -> str:
        return "delete_task"

    @property
    def description(self) -> str:
        return """Delete/remove a task from the user's list.

        Use this when user wants to DELETE, REMOVE, or GET RID OF a task.
        Recognize MANY ways people say this:
        - "Delete [task]", "Remove [task]", "Get rid of [task]"
        - "[Task] delete kar do", "[Task] hatado", "[Task] remove kar den"
        - "[Task] delete kerden", "[Task] delete kardo"
        - "I don't need [task] anymore", "Cancel [task]"
        - "Delete all [task]", "Sab [task] delete" → Delete ALL matching tasks

        Args:
            user_id: User ID who owns the task
            task_id: Exact ID (optional if title given)
            title: Task name to find (optional if task_id given)
            delete_all: Delete all matching tasks (default: false)

        Returns:
            Confirmation of task deletion
        """

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID who owns the task (auto-filled, do not provide)"
                },
                "task_id": {
                    "type": "string",
                    "description": "Exact task ID to delete"
                },
                "title": {
                    "type": "string",
                    "description": "Task title to search for"
                },
                "delete_all": {
                    "type": "boolean",
                    "description": "Delete all matching tasks (used when user says 'all', 'sab', 'sare')",
                    "default": False
                }
            }
        }

    def execute(
        self,
        user_id: str,
        session: Session = None,
        task_id: Optional[str] = None,
        title: Optional[str] = None,
        delete_all: bool = False,
        **kwargs
    ) -> MCPToolResponse:
        """
        Execute task deletion.

        Args:
            user_id: User ID who owns the task
            session: Database session
            task_id: Exact task ID to delete
            title: Task title to search
            require_confirmation: Whether to require clarification for matches
            **kwargs: Additional parameters (ignored)

        Returns:
            MCPToolResponse with deletion confirmation or matching options
        """
        try:
            # Validate inputs
            if not task_id and not title:
                raise ValidationError("Either task_id or title must be provided")

            if not session:
                raise ValidationError("Database session required")

            # Delete by ID (most precise)
            if task_id:
                return self._delete_by_id(task_id, user_id, session)

            # Delete by title (may have multiple matches)
            if title:
                return self._delete_by_title(title, user_id, session, delete_all)

        except (ValidationError, NotFoundError, OwnershipError) as e:
            return MCPToolResponse(
                success=False,
                error={"code": e.code, "message": e.message}
            )
        except Exception as e:
            return MCPToolResponse(
                success=False,
                error={"code": "INTERNAL_ERROR", "message": f"Failed to delete task: {str(e)}"}
            )

    def _delete_by_id(self, task_id: str, user_id: str, session: Session) -> MCPToolResponse:
        """Delete task by exact ID"""
        # Query task
        statement = select(Task).where(Task.id == task_id)
        task = session.execute(statement).scalar()

        if not task:
            raise NotFoundError(f"Task {task_id} not found")

        # Verify ownership
        if task.user_id != user_id:
            raise OwnershipError("Access denied to this task")

        # Store title for response
        task_title = task.title

        # Delete task
        session.delete(task)
        session.commit()

        return MCPToolResponse(
            success=True,
            data={
                "task_id": task_id,
                "title": task_title,
                "message": f"Deleted '{task_title}' from your tasks"
            }
        )

    def _delete_by_title(
        self,
        title: str,
        user_id: str,
        session: Session,
        delete_all: bool = False
    ) -> MCPToolResponse:
        """Delete task by title (handles multiple matches)"""
        # Search for matching tasks
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.title.ilike(f"%{title}%")
        )
        tasks = list(session.execute(statement).scalars().all())

        if not tasks:
            raise NotFoundError(f"No tasks found matching '{title}'")

        # Single match - delete it
        if len(tasks) == 1:
            task = tasks[0]
            task_title = task.title
            task_id = task.id

            session.delete(task)
            session.commit()

            return MCPToolResponse(
                success=True,
                data={
                    "task_id": task_id,
                    "title": task_title,
                    "message": f"Deleted '{task_title}' from your tasks"
                }
            )

        # Multiple matches
        if delete_all:
            # Delete ALL matching tasks
            deleted_count = 0
            deleted_titles = []
            for task in tasks:
                deleted_titles.append(task.title)
                session.delete(task)
                deleted_count += 1

            session.commit()

            return MCPToolResponse(
                success=True,
                data={
                    "deleted_count": deleted_count,
                    "titles": deleted_titles,
                    "message": f"Deleted {deleted_count} task(s) matching '{title}'"
                }
            )
        else:
            # Return options for clarification
            matching_tasks = []
            for task in tasks:
                matching_tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description
                })

            return MCPToolResponse(
                success=True,
                data={
                    "multiple_matches": True,
                    "tasks": matching_tasks,
                    "message": f"Found {len(tasks)} tasks matching '{title}'. Which one would you like to delete? (Say 'delete all' to delete all of them)"
                }
            )
