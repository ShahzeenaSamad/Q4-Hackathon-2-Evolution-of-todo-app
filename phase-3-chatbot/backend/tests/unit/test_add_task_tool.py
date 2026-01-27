"""
Contract Tests for Add Task MCP Tool

Validates that the AddTaskTool MCP tool adheres to its contract:
- Creates tasks with valid title and user_id
- Validates input parameters
- Returns proper success/error responses
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.orm import sessionmaker

from mcp_tools.add_task import AddTaskTool
from mcp_tools.base import MCPToolResponse
from mcp_tools.exceptions import ValidationError
from models import Task  # Use actual Task model from models


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test_add_task.db"


@pytest.fixture
def db_session():
    """Create a test database session"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def add_task_tool():
    """Provide AddTaskTool instance"""
    return AddTaskTool()


class TestAddTaskToolContract:
    """Contract tests for AddTaskTool"""

    def test_tool_has_correct_name(self, add_task_tool):
        """Test: Tool has correct name property"""
        assert add_task_tool.name == "add_task"

    def test_tool_has_description(self, add_task_tool):
        """Test: Tool provides description"""
        description = add_task_tool.description
        assert description is not None
        assert len(description) > 0
        assert "create" in description.lower() or "add" in description.lower()

    def test_tool_has_parameters(self, add_task_tool):
        """Test: Tool defines required parameters"""
        params = add_task_tool.parameters

        assert params is not None
        assert "type" in params
        assert params["type"] == "object"
        assert "properties" in params

        # Check required parameters
        assert "user_id" in params["properties"]
        assert "title" in params["properties"]

        # Check user_id is required
        user_id_prop = params["properties"]["user_id"]
        assert "required" in params
        assert "user_id" in params["required"]

    def test_execute_success_with_valid_inputs(self, db_session, add_task_tool):
        """Test: Can successfully create a task with valid inputs"""
        # Arrange
        user_id = "test_user_123"
        title = "Buy groceries"
        description = "Get milk, eggs, and bread"

        # Act
        result = add_task_tool.execute(
            user_id=user_id,
            title=title,
            description=description,
            session=db_session
        )

        # Assert
        assert isinstance(result, MCPToolResponse)
        assert result.success is True
        assert result.data is not None
        assert "task_id" in result.data
        assert result.data["title"] == title
        assert result.data["completed"] == False

    def test_execute_requires_title(self, db_session, add_task_tool):
        """Test: Validates empty title"""
        # Arrange
        user_id = "test_user_123"

        # Act
        result = add_task_tool.execute(
            user_id=user_id,
            title="",  # Empty title
            session=db_session
        )

        # Assert - should return error response
        assert result.success is False
        assert result.error is not None
        assert "title" in result.error["message"].lower() or "empty" in result.error["message"].lower()

    def test_execute_requires_user_id(self, db_session, add_task_tool):
        """Test: Validates missing user_id"""
        # Arrange
        title = "Test task"

        # Act
        result = add_task_tool.execute(
            user_id="",  # Empty user_id
            title=title,
            session=db_session
        )

        # Assert - should return error response
        assert result.success is False
        assert result.error is not None
        assert "user_id" in result.error["message"].lower() or "empty" in result.error["message"].lower()

    def test_execute_respects_session_parameter(self, add_task_tool):
        """Test: Requires database session"""
        # Arrange
        user_id = "test_user_123"
        title = "Test task"

        # Act - passing None for session
        result = add_task_tool.execute(
            user_id=user_id,
            title=title,
            session=None
        )

        # Assert - should return error response
        assert result.success is False
        assert result.error is not None
        assert "session" in result.error["message"].lower() or "required" in result.error["message"].lower()

    def test_execute_returns_structured_success_response(self, db_session, add_task_tool):
        """Test: Success response contains expected fields"""
        # Arrange
        user_id = "test_user_123"
        title = "Test task"

        # Act
        result = add_task_tool.execute(
            user_id=user_id,
            title=title,
            session=db_session
        )

        # Assert
        assert result.success is True
        assert result.data["task_id"] is not None
        assert isinstance(result.data["task_id"], int)
        assert result.data["title"] == title
        assert isinstance(result.data["completed"], bool)
        assert "created_at" in result.data

    def test_execute_handles_title_too_long(self, db_session, add_task_tool):
        """Test: Rejects title exceeding 200 characters"""
        # Arrange
        user_id = "test_user_123"
        title = "A" * 201  # 201 characters (exceeds 200 limit)

        # Act
        result = add_task_tool.execute(
            user_id=user_id,
            title=title,
            session=db_session
        )

        # Assert - should return error response
        assert result.success is False
        assert result.error is not None
        assert "200" in result.error["message"].lower() or "character" in result.error["message"].lower()

    def test_execute_handles_description_too_long(self, db_session, add_task_tool):
        """Test: Rejects description exceeding 2000 characters"""
        # Arrange
        user_id = "test_user_123"
        title = "Valid task"
        description = "A" * 2001  # 2001 characters (exceeds 2000 limit)

        # Act
        result = add_task_tool.execute(
            user_id=user_id,
            title=title,
            description=description,
            session=db_session
        )

        # Assert - should return error response
        assert result.success is False
        assert result.error is not None
        assert "2000" in result.error["message"].lower() or "character" in result.error["message"].lower()


class TestAddTaskToolIntegration:
    """Integration tests for AddTaskTool"""

    def test_create_multiple_tasks_in_sequence(self, db_session, add_task_tool):
        """Test: Can create multiple tasks for same user"""
        # Arrange
        user_id = "test_user_123"

        # Act
        task1 = add_task_tool.execute(
            user_id=user_id,
            title="First task",
            session=db_session
        )
        task2 = add_task_tool.execute(
            user_id=user_id,
            title="Second task",
            session=db_session
        )
        task3 = add_task_tool.execute(
            user_id=user_id,
            title="Third task",
            session=db_session
        )

        # Assert
        assert task1.success is True
        assert task2.success is True
        assert task3.success is True

        # Verify different task IDs
        task_ids = [task1.data["task_id"], task2.data["task_id"], task3.data["task_id"]]
        assert len(set(task_ids)) == 3  # All unique

    def test_tasks_persist_in_database(self, db_session, add_task_tool):
        """Test: Created tasks are actually stored in database"""
        # Arrange
        user_id = "test_user_123"
        title = "Persistent task"

        # Act
        result = add_task_tool.execute(
            user_id=user_id,
            title=title,
            session=db_session
        )
        db_session.commit()

        # Query database directly
        from sqlalchemy import select
        statement = select(Task).where(Task.user_id == user_id, Task.title == title)
        stored_task = db_session.execute(statement).scalar_one_or_none()

        # Assert
        assert stored_task is not None
        assert stored_task.title == title
        assert stored_task.user_id == user_id
        assert stored_task.completed == False
