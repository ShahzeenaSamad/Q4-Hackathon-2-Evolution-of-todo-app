"""
Add Task MCP Tool
Creates a new task for the user
"""

from typing import Dict, Any
from sqlmodel import Session, select

from mcp_tools.base import MCPTool, MCPToolResponse
from mcp_tools.exceptions import ValidationError, OwnershipError
from models import Task


class AddTaskTool(MCPTool):
    """
    MCP tool for creating new tasks.

    Allows users to add tasks through natural language by extracting
    task title and optional description from the agent's input.
    """

    @property
    def name(self) -> str:
        return "add_task"

    @property
    def description(self) -> str:
        return """Create a new todo task for the user.

        Use this when the user wants to ADD, CREATE, or MAKE a new task.
        Be VERY flexible - users phrase this in many ways:
        - "Add X", "Create task X", "Make a task for X"
        - "Project X ka task", "Task add kar do", "I need to X"
        - "Remind me to X", "Don't forget X", "I have to do X"
        - "X ka task bana do", "Task X create"

        Extract the main task/activity from what they say.

        Args:
            user_id: User ID who owns this task
            title: What the task is (required, max 200 chars)
            description: Optional extra details (max 2000 chars)

        Returns:
            Created task with confirmation
        """

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID who owns this task (auto-filled, do not provide)"
                },
                "title": {
                    "type": "string",
                    "description": "Task title (what needs to be done)",
                    "maxLength": 200
                },
                "description": {
                    "type": "string",
                    "description": "Optional additional details about the task",
                    "maxLength": 2000
                }
            },
            "required": ["title"]  # Only title is required from user input
        }

    def execute(self, user_id: str, title: str, description: str = None, session: Session = None, **kwargs) -> MCPToolResponse:
        """
        Execute task creation.

        Args:
            user_id: User ID who owns this task
            title: Task title
            description: Optional task description
            session: Database session (optional, for dependency injection)
            **kwargs: Additional parameters (ignored)

        Returns:
            MCPToolResponse with created task data
        """
        try:
            # Validate inputs
            self._validate_title(title)
            self._validate_user_id(user_id)
            self._validate_description(description)

            # Create task
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )

            if session:
                session.add(task)
                session.commit()
                session.refresh(task)
            else:
                # If no session provided, raise error (caller must provide session)
                raise ValidationError("Database session required")

            return MCPToolResponse(
                success=True,
                data={
                    "task_id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at)
                }
            )

        except (ValidationError, OwnershipError) as e:
            return MCPToolResponse(
                success=False,
                error={"code": e.code, "message": e.message}
            )
        except Exception as e:
            return MCPToolResponse(
                success=False,
                error={"code": "INTERNAL_ERROR", "message": f"Failed to create task: {str(e)}"}
            )

    def _validate_title(self, title: str) -> None:
        """Validate task title"""
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        if len(title) > 200:
            raise ValidationError("Task title cannot exceed 200 characters")

    def _validate_user_id(self, user_id: str) -> None:
        """Validate user ID"""
        if not user_id or not user_id.strip():
            raise ValidationError("User ID cannot be empty")

    def _validate_description(self, description: str) -> None:
        """Validate task description"""
        if description and len(description) > 2000:
            raise ValidationError("Task description cannot exceed 2000 characters")
