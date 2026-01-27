"""
Complete Task MCP Tool
Marks a task as completed
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select

from mcp_tools.base import MCPTool, MCPToolResponse
from mcp_tools.exceptions import ValidationError, NotFoundError, OwnershipError
from models import Task


class CompleteTaskTool(MCPTool):
    """
    MCP tool for marking tasks as completed.

    Allows users to complete tasks by ID or by matching title.
    Handles disambiguation when multiple tasks match.
    """

    @property
    def name(self) -> str:
        return "complete_task"

    @property
    def description(self) -> str:
        return """Mark a task as completed/done.

        Use this when user FINISHED, COMPLETED, or DID a task.
        Recognize MANY ways people say this:
        - "I finished X", "Done with X", "X is complete"
        - "X ho gaya", "X complete", "X done"
        - "Finished my workout", "Task complete", "Mark X as done"
        - "X kar liya", "X complete ho gaya"

        Args:
            user_id: User ID who owns the task
            task_id: Exact ID (optional if title given)
            title: Task name to find (optional if task_id given)

        Returns:
            Confirmation of task completion
        """

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID who owns the task"
                },
                "task_id": {
                    "type": "string",
                    "description": "Exact task ID to complete"
                },
                "title": {
                    "type": "string",
                    "description": "Task title to search for"
                },
                "require_confirmation": {
                    "type": "boolean",
                    "description": "Require clarification for multiple matches",
                    "default": True
                }
            }
        }

    def execute(
        self,
        user_id: str,
        session: Session = None,
        task_id: Optional[str] = None,
        title: Optional[str] = None,
        require_confirmation: bool = True,
        **kwargs
    ) -> MCPToolResponse:
        """
        Execute task completion.

        Args:
            user_id: User ID who owns the task
            session: Database session
            task_id: Exact task ID to complete
            title: Task title to search
            require_confirmation: Whether to require clarification for matches
            **kwargs: Additional parameters (ignored)

        Returns:
            MCPToolResponse with completed task or matching options
        """
        try:
            # Validate inputs
            if not task_id and not title:
                raise ValidationError("Either task_id or title must be provided")

            if not session:
                raise ValidationError("Database session required")

            # Complete by ID (most precise)
            if task_id:
                return self._complete_by_id(task_id, user_id, session)

            # Complete by title (may have multiple matches)
            if title:
                return self._complete_by_title(title, user_id, session, require_confirmation)

        except (ValidationError, NotFoundError, OwnershipError) as e:
            return MCPToolResponse(
                success=False,
                error={"code": e.code, "message": e.message}
            )
        except Exception as e:
            return MCPToolResponse(
                success=False,
                error={"code": "INTERNAL_ERROR", "message": f"Failed to complete task: {str(e)}"}
            )

    def _complete_by_id(self, task_id: str, user_id: str, session: Session) -> MCPToolResponse:
        """Complete task by exact ID"""
        # Query task
        statement = select(Task).where(Task.id == task_id)
        task = session.execute(statement).scalar()

        if not task:
            raise NotFoundError(f"Task {task_id} not found")

        # Verify ownership
        if task.user_id != user_id:
            raise OwnershipError("Access denied to this task")

        # Mark as completed
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        return MCPToolResponse(
            success=True,
            data={
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed,
                "message": f"Marked '{task.title}' as complete"
            }
        )

    def _complete_by_title(
        self,
        title: str,
        user_id: str,
        session: Session,
        require_confirmation: bool
    ) -> MCPToolResponse:
        """Complete task by title (handles multiple matches)"""
        # Search for matching tasks
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.title.ilike(f"%{title}%"),
            Task.completed == False
        )
        tasks = list(session.execute(statement).scalars().all())

        if not tasks:
            raise NotFoundError(f"No pending tasks found matching '{title}'")

        # Single match - complete it
        if len(tasks) == 1:
            task = tasks[0]
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return MCPToolResponse(
                success=True,
                data={
                    "task_id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "message": f"Marked '{task.title}' as complete"
                }
            )

        # Multiple matches - return options for clarification
        if require_confirmation:
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
                    "message": f"Found {len(tasks)} tasks matching '{title}'. Which one would you like to complete?"
                }
            )

        # Auto-complete first match (if confirmation not required)
        task = tasks[0]
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        return MCPToolResponse(
            success=True,
            data={
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed,
                "message": f"Marked '{task.title}' as complete"
            }
        )
