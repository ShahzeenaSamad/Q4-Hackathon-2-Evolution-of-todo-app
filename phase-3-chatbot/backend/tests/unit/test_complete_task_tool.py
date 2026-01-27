"""
Contract Tests for Complete Task MCP Tool

Validates that the CompleteTaskTool MCP tool adheres to its contract:
- Completes tasks by task_id
- Completes tasks by title (with disambiguation)
- Validates ownership
- Handles edge cases (already completed, not found, etc.)
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.orm import sessionmaker

from mcp_tools.complete_task import CompleteTaskTool
from mcp_tools.base import MCPToolResponse
from mcp_tools.exceptions import ValidationError, NotFoundError, OwnershipError
from models import Task  # Use actual Task model from models


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test_complete_task.db"


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
def complete_task_tool():
    """Provide CompleteTaskTool instance"""
    return CompleteTaskTool()


@pytest.fixture
def populated_session(db_session):
    """Create a session with sample tasks"""
    # Pending tasks
    task1 = Task(user_id="test_user_123", title="Buy groceries", completed=False)
    task2 = Task(user_id="test_user_123", title="Walk the dog", completed=False)
    task3 = Task(user_id="test_user_123", title="Buy milk", completed=False)

    # Already completed task
    task4 = Task(user_id="test_user_123", title="Do laundry", completed=True)

    # Different user's task
    task5 = Task(user_id="other_user_456", title="Other user task", completed=False)

    db_session.add_all([task1, task2, task3, task4, task5])
    db_session.commit()

    return db_session


class TestCompleteTaskToolContract:
    """Contract tests for CompleteTaskTool"""

    def test_tool_has_correct_name(self, complete_task_tool):
        """Test: Tool has correct name property"""
        assert complete_task_tool.name == "complete_task"

    def test_tool_has_description(self, complete_task_tool):
        """Test: Tool provides description"""
        description = complete_task_tool.description
        assert description is not None
        assert len(description) > 0
        assert any(word in description.lower() for word in ["complete", "finish", "mark"])

    def test_tool_has_parameters(self, complete_task_tool):
        """Test: Tool defines required parameters"""
        params = complete_task_tool.parameters

        assert params is not None
        assert "type" in params
        assert params["type"] == "object"
        assert "properties" in params

        # Check parameters exist
        assert "user_id" in params["properties"]
        assert "task_id" in params["properties"]
        assert "title" in params["properties"]
        assert "require_confirmation" in params["properties"]

    def test_execute_requires_task_id_or_title(self, db_session, complete_task_tool):
        """Test: Validates that either task_id or title is provided"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            task_id=None,
            title=None,
            session=db_session
        )

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "task_id" in result.error["message"].lower() or "title" in result.error["message"].lower()

    def test_execute_respects_session_parameter(self, complete_task_tool):
        """Test: Requires database session"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            task_id="1",
            session=None
        )

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "session" in result.error["message"].lower() or "required" in result.error["message"].lower()


class TestCompleteByTaskId:
    """Tests for completing task by exact ID"""

    def test_complete_by_valid_task_id(self, populated_session, complete_task_tool):
        """Test: Can complete a task by valid ID"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            task_id="1",
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert result.data["task_id"] == 1
        assert result.data["completed"] is True
        assert "marked" in result.data["message"].lower() or "complete" in result.data["message"].lower()

    def test_complete_verifies_ownership(self, populated_session, complete_task_tool):
        """Test: Cannot complete another user's task"""
        # Act - try to complete task belonging to other_user_456
        result = complete_task_tool.execute(
            user_id="test_user_123",
            task_id="5",  # Task 5 belongs to other_user_456
            session=populated_session
        )

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "access" in result.error["message"].lower() or "denied" in result.error["message"].lower()

    def test_complete_handles_nonexistent_task_id(self, db_session, complete_task_tool):
        """Test: Handles invalid task ID gracefully"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            task_id="999",  # Non-existent task
            session=db_session
        )

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "not found" in result.error["message"].lower()

    def test_complete_already_completed_task(self, populated_session, complete_task_tool):
        """Test: Can mark an already completed task as complete (idempotent)"""
        # Act - task 4 is already completed
        result = complete_task_tool.execute(
            user_id="test_user_123",
            task_id="4",
            session=populated_session
        )

        # Assert - should still succeed
        assert result.success is True
        assert result.data["completed"] is True


class TestCompleteByTitle:
    """Tests for completing task by title"""

    def test_complete_by_exact_title_match(self, populated_session, complete_task_tool):
        """Test: Can complete task by exact title"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            title="Walk the dog",
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert result.data["title"] == "Walk the dog"
        assert result.data["completed"] is True

    def test_complete_by_partial_title_match(self, populated_session, complete_task_tool):
        """Test: Can complete task by partial title"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            title="milk",  # Should match "Buy milk"
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert "milk" in result.data["title"].lower()
        assert result.data["completed"] is True

    def test_complete_by_title_returns_multiple_matches(self, populated_session, complete_task_tool):
        """Test: Returns clarification options when multiple tasks match"""
        # Act - both "Buy groceries" and "Buy milk" match "buy"
        result = complete_task_tool.execute(
            user_id="test_user_123",
            title="buy",
            require_confirmation=True,
            session=populated_session
        )

        # Assert
        assert result.success is True
        assert result.data.get("multiple_matches") is True
        assert "tasks" in result.data
        assert len(result.data["tasks"]) == 2  # Two matches

    def test_complete_by_title_auto_completes_when_confirmation_disabled(self, populated_session, complete_task_tool):
        """Test: Auto-completes first match when confirmation disabled"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            title="buy",
            require_confirmation=False,
            session=populated_session
        )

        # Assert - should complete first match
        assert result.success is True
        assert result.data.get("multiple_matches") is not True  # Not asking for clarification
        assert result.data["completed"] is True

    def test_complete_by_title_handles_no_matches(self, db_session, complete_task_tool):
        """Test: Handles no matching tasks gracefully"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            title="nonexistent task",
            session=db_session
        )

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "not found" in result.error["message"].lower() or "no pending" in result.error["message"].lower()

    def test_complete_by_title_only_searches_pending_tasks(self, populated_session, complete_task_tool):
        """Test: Only searches pending tasks, ignores completed ones"""
        # Act - "Do laundry" is already completed
        result = complete_task_tool.execute(
            user_id="test_user_123",
            title="laundry",
            session=populated_session
        )

        # Assert - should not find the completed task
        assert result.success is False
        assert result.error is not None


class TestCompleteTaskToolIntegration:
    """Integration tests for CompleteTaskTool"""

    def test_completed_task_persists_in_database(self, populated_session, complete_task_tool):
        """Test: Completed task is actually updated in database"""
        # Act
        complete_task_tool.execute(
            user_id="test_user_123",
            task_id="1",
            session=populated_session
        )

        # Query database directly
        from sqlalchemy import select
        statement = select(Task).where(Task.id == 1)
        task = populated_session.execute(statement).scalar_one_or_none()

        # Assert
        assert task is not None
        assert task.completed is True

    def test_can_complete_multiple_tasks(self, populated_session, complete_task_tool):
        """Test: Can complete multiple tasks in sequence"""
        # Act
        result1 = complete_task_tool.execute(
            user_id="test_user_123",
            task_id="1",
            session=populated_session
        )

        result2 = complete_task_tool.execute(
            user_id="test_user_123",
            task_id="2",
            session=populated_session
        )

        # Assert
        assert result1.success is True
        assert result2.success is True
        assert result1.data["task_id"] == 1
        assert result2.data["task_id"] == 2

    def test_title_search_is_case_insensitive(self, populated_session, complete_task_tool):
        """Test: Title search works with different cases"""
        # Act
        result = complete_task_tool.execute(
            user_id="test_user_123",
            title="GROCERIES",  # Uppercase
            session=populated_session
        )

        # Assert - should match "Buy groceries"
        assert result.success is True
        assert "groceries" in result.data["title"].lower()
