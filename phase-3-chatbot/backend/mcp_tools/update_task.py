"""
Update Task MCP Tool
Modifies an existing task's title or description
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select

from mcp_tools.base import MCPTool, MCPToolResponse
from mcp_tools.exceptions import ValidationError, NotFoundError, OwnershipError
from models import Task


class UpdateTaskTool(MCPTool):
    """
    MCP tool for updating tasks.

    Allows users to modify task title or description.
    Handles disambiguation when multiple tasks match.
    """

    @property
    def name(self) -> str:
        return "update_task"

    @property
    def description(self) -> str:
        return """Update/modify an existing task.

        Use this when user wants to EDIT, UPDATE, CHANGE, or MODIFY a task.
        Recognize MANY ways people say this:
        - "Change [task] to [...]", "Update [task]", "Edit [task]"
        - "[Task] edit kar do", "[Task] change kar den", "[Task] update kerden"
        - "[Task] ko [...] bana do", "Modify [task]"
        - "Change [task] description to [...]", "Edit [task] title"

        Args:
            user_id: User ID who owns the task
            task_id: Exact ID (optional if title given)
            title: Current task name to find (optional if task_id given)
            new_title: New title for the task
            new_description: New description for the task

        Returns:
            Confirmation of task update
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
                    "description": "Exact task ID to update"
                },
                "title": {
                    "type": "string",
                    "description": "Current task title to search for"
                },
                "new_title": {
                    "type": "string",
                    "description": "New title for the task"
                },
                "new_description": {
                    "type": "string",
                    "description": "New description for the task"
                },
                "update_all": {
                    "type": "boolean",
                    "description": "Update all matching tasks (used when user says 'all', 'sab')",
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
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        update_all: bool = False,
        **kwargs
    ) -> MCPToolResponse:
        """
        Execute task update.

        Args:
            user_id: User ID who owns the task
            session: Database session
            task_id: Exact task ID to update
            title: Current task title to search
            new_title: New title for the task
            new_description: New description for the task
            update_all: Update all matching tasks
            **kwargs: Additional parameters (ignored)

        Returns:
            MCPToolResponse with update confirmation or matching options
        """
        try:
            # Validate inputs
            if not task_id and not title:
                raise ValidationError("Either task_id or title must be provided")

            if not new_title and not new_description:
                raise ValidationError("Either new_title or new_description must be provided")

            if not session:
                raise ValidationError("Database session required")

            # Update by ID (most precise)
            if task_id:
                return self._update_by_id(task_id, user_id, session, new_title, new_description)

            # Update by title (may have multiple matches)
            if title:
                return self._update_by_title(title, user_id, session, new_title, new_description, update_all)

        except (ValidationError, NotFoundError, OwnershipError) as e:
            return MCPToolResponse(
                success=False,
                error={"code": e.code, "message": e.message}
            )
        except Exception as e:
            return MCPToolResponse(
                success=False,
                error={"code": "INTERNAL_ERROR", "message": f"Failed to update task: {str(e)}"}
            )

    def _update_by_id(
        self,
        task_id: str,
        user_id: str,
        session: Session,
        new_title: Optional[str],
        new_description: Optional[str]
    ) -> MCPToolResponse:
        """Update task by exact ID"""
        # Query task
        statement = select(Task).where(Task.id == task_id)
        task = session.execute(statement).scalar()

        if not task:
            raise NotFoundError(f"Task {task_id} not found")

        # Verify ownership
        if task.user_id != user_id:
            raise OwnershipError("Access denied to this task")

        # Store old title for response
        old_title = task.title

        # Update fields
        if new_title:
            task.title = new_title
        if new_description:
            task.description = new_description

        session.add(task)
        session.commit()
        session.refresh(task)

        # Build message
        if new_title and new_description:
            message = f"Updated '{old_title}': title changed to '{new_title}' and description updated"
        elif new_title:
            message = f"Changed task name from '{old_title}' to '{new_title}'"
        else:
            message = f"Updated '{task.title}' description"

        return MCPToolResponse(
            success=True,
            data={
                "task_id": task.id,
                "title": task.title,
                "old_title": old_title,
                "description": task.description,
                "message": message
            }
        )

    def _update_by_title(
        self,
        title: str,
        user_id: str,
        session: Session,
        new_title: Optional[str],
        new_description: Optional[str],
        update_all: bool
    ) -> MCPToolResponse:
        """Update task by title (handles multiple matches)"""
        # Search for matching tasks
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.title.ilike(f"%{title}%")
        )
        tasks = list(session.execute(statement).scalars().all())

        if not tasks:
            raise NotFoundError(f"No tasks found matching '{title}'")

        # Single match - update it
        if len(tasks) == 1:
            task = tasks[0]
            old_title = task.title

            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description

            session.add(task)
            session.commit()
            session.refresh(task)

            return MCPToolResponse(
                success=True,
                data={
                    "task_id": task.id,
                    "title": task.title,
                    "old_title": old_title,
                    "description": task.description,
                    "message": f"Updated '{old_title}' to '{task.title}'"
                }
            )

        # Multiple matches
        if update_all:
            # Update ALL matching tasks
            updated_count = 0
            for task in tasks:
                if new_title:
                    task.title = new_title
                if new_description:
                    task.description = new_description
                session.add(task)
                updated_count += 1

            session.commit()

            return MCPToolResponse(
                success=True,
                data={
                    "updated_count": updated_count,
                    "new_title": new_title,
                    "new_description": new_description,
                    "message": f"Updated {updated_count} task(s) matching '{title}'"
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
                    "message": f"Found {len(tasks)} tasks matching '{title}'. Which one would you like to update? (Say 'update all' to update all of them)"
                }
            )
