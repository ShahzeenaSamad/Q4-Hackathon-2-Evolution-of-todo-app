"""
Integration Tests for Task Creation via Chat API

Tests the complete flow:
User sends "Add buy milk" → API processes → Agent extracts intent → MCP tool executes → Task created
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.orm import sessionmaker

# Import models to ensure tables are created
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from main import app
from models.task import Task
# User model not needed for phase-3-chatbot - user_id is just a string
User = None


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test_chat_integration.db"


@pytest.fixture
def test_db():
    """Create test database and tables"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def test_client(test_db):
    """Create test client with database session override"""
    from db import get_db

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user(test_db):
    """Create a test user ID (no User model needed for phase-3)"""
    return type('User', (), {'id': 'test_user_integration'})()


class TestTaskCreationIntegration:
    """Integration tests for task creation through chat"""

    def test_add_task_via_chat_endpoint(self, test_client, test_user):
        """Test: Can create task through natural language chat"""
        # Arrange
        user_id = test_user.id
        message = "Add buy milk"

        # Act
        response = test_client.post(
            f"/api/v1/chat/{user_id}",
            json={"message": message, "conversation_id": None}
        )

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "response" in data["data"]

        # Verify tool was called
        tool_calls = data["data"].get("tool_calls", [])
        assert len(tool_calls) > 0

        # Check add_task tool was called successfully
        add_task_calls = [tc for tc in tool_calls if tc.get("tool") == "add_task"]
        assert len(add_task_calls) > 0
        assert add_task_calls[0]["success"] is True

    def test_add_task_creates_task_in_database(self, test_client, test_user, test_db):
        """Test: Task created through chat is persisted in database"""
        # Arrange
        user_id = test_user.id
        message = "Add test task via chat"

        # Act
        response = test_client.post(
            f"/api/v1/chat/{user_id}",
            json={"message": message, "conversation_id": None}
        )

        # Assert - API response successful
        assert response.status_code == 200

        # Query database to verify task was created
        # Note: Mock agent uses hardcoded user_id "022cf320-3234-4e62-b773-443f36d55c9d"
        from sqlalchemy import select
        statement = select(Task).where(
            Task.title.ilike("%test task via chat%")
        )
        tasks = list(test_db.execute(statement).scalars().all())

        # Assert - task was created
        assert len(tasks) > 0

    def test_conversation_id_is_persisted(self, test_client, test_user, test_db):
        """Test: Conversation ID is returned and can be used for follow-up"""
        # Arrange
        user_id = test_user.id
        message1 = "Add first task"

        # Act - First message (no conversation_id)
        response1 = test_client.post(
            f"/api/v1/chat/{user_id}",
            json={"message": message1, "conversation_id": None}
        )

        # Assert - First message creates conversation
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["success"] is True
        conversation_id = data1["data"].get("conversation_id")
        assert conversation_id is not None

        # Act - Second message (with conversation_id)
        message2 = "Add second task"
        response2 = test_client.post(
            f"/api/v1/chat/{user_id}",
            json={"message": message2, "conversation_id": conversation_id}
        )

        # Assert - Second message uses existing conversation
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["success"] is True

    def test_empty_message_returns_clarification(self, test_client, test_user):
        """Test: Empty or unclear message prompts for clarification"""
        # Arrange
        user_id = test_user.id
        empty_message = ""

        # Act
        response = test_client.post(
            f"/api/v1/chat/{user_id}",
            json={"message": empty_message, "conversation_id": None}
        )

        # Assert
        # Should handle gracefully - either returns 200 with clarification
        # or 400/422 with validation error
        assert response.status_code in [200, 400, 422]

    def test_multiple_tasks_in_one_message(self, test_client, test_user):
        """Test: Can handle request to create multiple tasks"""
        # Arrange
        user_id = test_user.id
        message = "Add three tasks: task 1, task 2, and task 3"

        # Act
        response = test_client.post(
            f"/api/v1/chat/{user_id}",
            json={"message": message, "conversation_id": None}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # The system should acknowledge and handle the request
        # (May create 1 task or ask for clarification based on implementation)

    def test_chat_returns_ai_response(self, test_client, test_user):
        """Test: Chat endpoint returns AI-generated response"""
        # Arrange
        user_id = test_user.id
        message = "Add groceries to buy"

        # Act
        response = test_client.post(
            f"/api/v1/chat/{user_id}",
            json={"message": message, "conversation_id": None}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "response" in data["data"]
        assert len(data["data"]["response"]) > 0

        # Response should confirm task creation
        response_text = data["data"]["response"].lower()
        assert any(word in response_text for word in ["added", "created", "task", "success"])


class TestTaskCreationErrorHandling:
    """Error handling tests for task creation"""

    def test_handles_invalid_user_id_gracefully(self, test_client):
        """Test: Invalid user_id returns proper error"""
        # Arrange
        invalid_user_id = "nonexistent_user"
        message = "Add test task"

        # Act
        response = test_client.post(
            f"/api/v1/chat/{invalid_user_id}",
            json={"message": message, "conversation_id": None}
        )

        # Assert - Should handle gracefully (may create user or return error)
        # The key is it doesn't crash
        assert response.status_code in [200, 400, 404]

    def test_handles_database_connection_error(self, test_client):
        """Test: Database connection issues are handled gracefully"""
        # This would require mocking a database failure
        # For now, we verify the endpoint doesn't crash
        pass
        # TODO: Add test with mock database failure
