"""
Contract Tests for List Tasks MCP Tool

Validates that the ListTasksTool MCP tool adheres to its contract:
- Queries tasks with valid user_id
- Validates input parameters
- Returns proper success/error responses
- Supports filtering by completion status
- Handles empty task lists
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.orm import sessionmaker

from mcp_tools.list_tasks import ListTasksTool
from mcp_tools.base import MCPToolResponse
from mcp_tools.exceptions import ValidationError
from models import Task  # Use actual Task model from models


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test_list_tasks.db"


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
def list_tasks_tool():
    """Provide ListTasksTool instance"""
    return ListTasksTool()


@pytest.fixture
def populated_session(db_session):
    """Create a session with sample tasks"""
    # Create pending tasks
    task1 = Task(user_id="test_user_123", title="Buy groceries", completed=False)
    task2 = Task(user_id="test_user_123", title="Walk the dog", completed=False)
    task3 = Task(user_id="test_user_123", title="Do laundry", completed=True)

    # Create tasks for different user
    task4 = Task(user_id="other_user_456", title="Other user task", completed=False)

    db_session.add_all([task1, task2, task3, task4])
    db_session.commit()

    return db_session


class TestListTasksToolContract:
    """Contract tests for ListTasksTool"""

    def test_tool_has_correct_name(self, list_tasks_tool):
        """Test: Tool has correct name property"""
        assert list_tasks_tool.name == "list_tasks"

    def test_tool_has_description(self, list_tasks_tool):
        """Test: Tool provides description"""
        description = list_tasks_tool.description
        assert description is not None
        assert len(description) > 0
        assert any(word in description.lower() for word in ["query", "list", "show", "display"])

    def test_tool_has_parameters(self, list_tasks_tool):
        """Test: Tool defines required parameters"""
        params = list_tasks_tool.parameters

        assert params is not None
        assert "type" in params
        assert params["type"] == "object"
        assert "properties" in params

        # Check required parameters
        assert "user_id" in params["properties"]
        assert "completed" in params["properties"]
        assert "limit" in params["properties"]

        # Check user_id is required
        user_id_prop = params["properties"]["user_id"]
        assert "required" in params
        assert "user_id" in params["required"]

    def test_execute_requires_user_id(self, db_session, list_tasks_tool):
        """Test: Validates missing user_id"""
        # Act & Assert
        result = list_tasks_tool.execute(
            user_id="",  # Empty user_id
            session=db_session
        )

        # Should return error response (not raise exception)
        assert result.success is False
        assert result.error is not None
        assert "user_id" in result.error["message"].lower() or "empty" in result.error["message"].lower()

    def test_execute_respects_session_parameter(self, list_tasks_tool):
        """Test: Requires database session"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            session=None
        )

        # Assert - should return error response
        assert result.success is False
        assert result.error is not None
        assert "session" in result.error["message"].lower() or "required" in result.error["message"].lower()

    def test_execute_returns_structured_success_response(self, populated_session, list_tasks_tool):
        """Test: Success response contains expected fields"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert "tasks" in result.data
        assert "total" in result.data
        assert "pending" in result.data
        assert "completed" in result.data

        # Verify counts
        assert result.data["total"] == 3  # 3 tasks for test_user_123
        assert result.data["pending"] == 2  # 2 pending
        assert result.data["completed"] == 1  # 1 completed

    def test_execute_filters_by_completed_status(self, populated_session, list_tasks_tool):
        """Test: Can filter tasks by completion status"""
        # Act - get only pending tasks
        result_pending = list_tasks_tool.execute(
            user_id="test_user_123",
            completed=False,
            session=populated_session
        )

        # Assert
        assert result_pending.success is True
        assert len(result_pending.data["tasks"]) == 2  # 2 pending tasks
        assert all(not task["completed"] for task in result_pending.data["tasks"])

        # Act - get only completed tasks
        result_completed = list_tasks_tool.execute(
            user_id="test_user_123",
            completed=True,
            session=populated_session
        )

        # Assert
        assert result_completed.success is True
        assert len(result_completed.data["tasks"]) == 1  # 1 completed task
        assert all(task["completed"] for task in result_completed.data["tasks"])

    def test_execute_respects_limit_parameter(self, populated_session, list_tasks_tool):
        """Test: Respects limit parameter"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            limit=2,
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert len(result.data["tasks"]) == 2  # Limited to 2

    def test_execute_returns_task_with_all_fields(self, populated_session, list_tasks_tool):
        """Test: Returned tasks have all expected fields"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert len(result.data["tasks"]) > 0

        task = result.data["tasks"][0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task


class TestListTasksToolIntegration:
    """Integration tests for ListTasksTool"""

    def test_handles_empty_task_list(self, db_session, list_tasks_tool):
        """Test: Returns empty list gracefully when user has no tasks"""
        # Act
        result = list_tasks_tool.execute(
            user_id="nonexistent_user",
            session=db_session
        )

        # Assert
        assert result.success is True
        assert result.data["tasks"] == []
        assert result.data["total"] == 0
        assert result.data["pending"] == 0
        assert result.data["completed"] == 0

    def test_isolates_users_properly(self, populated_session, list_tasks_tool):
        """Test: User cannot see other users' tasks"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            session=populated_session
        )

        # Assert - should not see other_user_456's task
        assert result.success is True
        assert len(result.data["tasks"]) == 3  # Only test_user_123's tasks
        assert all(task["id"] != 4 for task in result.data["tasks"])

    def test_tasks_ordered_by_created_at(self, populated_session, list_tasks_tool):
        """Test: Tasks are returned in creation order"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            session=populated_session
        )

        # Assert - verify ordering
        assert result.success is True
        # Tasks should be ordered by created_at ascending
        # (task IDs are auto-incrementing, so they reflect creation order)
        task_ids = [task["id"] for task in result.data["tasks"]]
        assert task_ids == sorted(task_ids)

    def test_counts_are_accurate(self, populated_session, list_tasks_tool):
        """Test: Total counts match actual database state"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            session=populated_session
        )

        # Assert
        assert result.success is True
        # Counts should match what we created in fixture
        assert result.data["total"] == 3
        assert result.data["pending"] == 2
        assert result.data["completed"] == 1

    def test_limit_parameter_does_not_affect_counts(self, populated_session, list_tasks_tool):
        """Test: Limit parameter affects returned tasks but not counts"""
        # Act
        result = list_tasks_tool.execute(
            user_id="test_user_123",
            limit=1,
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert len(result.data["tasks"]) == 1  # Only 1 task returned
        assert result.data["total"] == 3  # But counts show all tasks
