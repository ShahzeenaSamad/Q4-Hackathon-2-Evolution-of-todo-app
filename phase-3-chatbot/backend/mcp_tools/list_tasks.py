"""
List Tasks MCP Tool
Queries and displays user's tasks
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select

from mcp_tools.base import MCPTool, MCPToolResponse
from mcp_tools.exceptions import ValidationError
from models import Task


class ListTasksTool(MCPTool):
    """
    MCP tool for querying user tasks.

    Allows users to see their tasks, filter by completion status,
    and get task counts.
    """

    @property
    def name(self) -> str:
        return "list_tasks"

    @property
    def description(self) -> str:
        return """Show and list the user's todo tasks.

        Use this when the user wants to SEE, CHECK, or KNOW their tasks.
        Be VERY flexible with phrasing:
        - "What are my tasks?", "Show my tasks", "My todo list"
        - "Kya kaam hai?", "Meri tasks", "Pending tasks"
        - "What's pending?", "Kya baki hai?", "Tasks list"
        - "My work", "To-do list", "Kaun kaam baaki"

        Args:
            user_id: User ID to query tasks for
            completed: Optional - true for done tasks, false for pending
            limit: Optional - max tasks to show

        Returns:
            Task list with counts
        """

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID to query tasks for (auto-filled, do not provide)"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Optional filter by completion status"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tasks to return",
                    "default": 50
                }
            },
            "required": []  # Empty - we provide user_id from backend
        }

    def execute(
        self,
        user_id: str,
        completed: Optional[bool] = None,
        limit: int = 50,
        session: Session = None,
        **kwargs
    ) -> MCPToolResponse:
        """
        Execute task query.

        Args:
            user_id: User ID to query tasks for
            completed: Optional completion filter
            limit: Maximum tasks to return
            session: Database session
            **kwargs: Additional parameters (ignored)

        Returns:
            MCPToolResponse with task list and counts
        """
        try:
            # Validate inputs
            self._validate_user_id(user_id)

            if not session:
                raise ValidationError("Database session required")

            # Build query
            statement = select(Task).where(Task.user_id == user_id)

            # Apply completion filter if specified
            if completed is not None:
                statement = statement.where(Task.completed == completed)

            # Apply limit and order
            statement = statement.order_by(Task.created_at).limit(limit)

            # Execute query
            tasks = list(session.execute(statement).scalars().all())

            # Get counts
            count_statement = select(Task).where(Task.user_id == user_id)
            all_tasks = list(session.execute(count_statement).scalars().all())
            total = len(all_tasks)
            pending = sum(1 for t in all_tasks if not t.completed)
            completed_count = sum(1 for t in all_tasks if t.completed)

            # Format results
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at)
                })

            return MCPToolResponse(
                success=True,
                data={
                    "tasks": task_list,
                    "total": total,
                    "pending": pending,
                    "completed": completed_count
                }
            )

        except ValidationError as e:
            return MCPToolResponse(
                success=False,
                error={"code": e.code, "message": e.message}
            )
        except Exception as e:
            return MCPToolResponse(
                success=False,
                error={"code": "INTERNAL_ERROR", "message": f"Failed to query tasks: {str(e)}"}
            )

    def _validate_user_id(self, user_id: str) -> None:
        """Validate user ID"""
        if not user_id or not user_id.strip():
            raise ValidationError("User ID cannot be empty")
