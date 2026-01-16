#!/usr/bin/env python3
"""Test script for console-todo.py"""
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import classes directly by importing the module
import importlib.util
spec = importlib.util.spec_from_file_location("console_todo", os.path.join(os.path.dirname(__file__), "console-todo.py"))
console_todo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(console_todo)

Todo = console_todo.Todo
TodoStorage = console_todo.TodoStorage
TodoService = console_todo.TodoService
TodoCLI = console_todo.TodoCLI
from io import StringIO
from unittest.mock import patch
import time

def test_model_layer():
    """Test Model Layer"""
    print("\n=== Testing Model Layer ===")

    # Test Todo creation
    todo = Todo(1, "Test Task", "Test Description")
    assert todo.id == 1
    assert todo.title == "Test Task"
    assert todo.description == "Test Description"
    assert todo.completed == False
    print("✅ Todo creation works")

    # Test mark_completed
    todo.mark_completed()
    assert todo.completed == True
    print("✅ mark_completed() works")

    # Test mark_pending
    todo.mark_pending()
    assert todo.completed == False
    print("✅ mark_pending() works")

    # Test to_dict
    todo_dict = todo.to_dict()
    assert todo_dict['id'] == 1
    assert todo_dict['title'] == "Test Task"
    assert 'created_at' in todo_dict
    print("✅ to_dict() works")

def test_storage_layer():
    """Test Storage Layer"""
    print("\n=== Testing Storage Layer ===")

    storage = TodoStorage()

    # Test add
    todo = storage.add("Task 1", "Description 1")
    assert todo.id == 1
    assert len(storage.get_all()) == 1
    print("✅ add() works")

    # Test get_by_id
    found = storage.get_by_id(1)
    assert found is not None
    assert found.title == "Task 1"
    print("✅ get_by_id() works")

    # Test get_all
    storage.add("Task 2")
    todos = storage.get_all()
    assert len(todos) == 2
    print("✅ get_all() works")

    # Test update
    result = storage.update(1, title="Updated Task 1")
    assert result == True
    updated = storage.get_by_id(1)
    assert updated.title == "Updated Task 1"
    print("✅ update() works")

    # Test completed count
    storage.get_by_id(1).mark_completed()
    assert storage.get_completed_count() == 1
    assert storage.get_pending_count() == 1
    print("✅ get_completed_count() and get_pending_count() work")

    # Test delete
    result = storage.delete(1)
    assert result == True
    assert len(storage.get_all()) == 1
    print("✅ delete() works")

    # Test is_empty
    assert storage.is_empty() == False
    print("✅ is_empty() works")

def test_service_layer():
    """Test Service Layer"""
    print("\n=== Testing Service Layer ===")

    storage = TodoStorage()
    service = TodoService(storage)

    # Test create_todo
    todo = service.create_todo("Service Task", "Service Description")
    assert todo.id == 1
    print("✅ create_todo() works")

    # Test list_todos
    service.create_todo("Task 2")
    todos, completed, pending = service.list_todos()
    assert len(todos) == 2
    assert completed == 0
    assert pending == 2
    print("✅ list_todos() works")

    # Test update_todo
    result = service.update_todo(1, "Updated Service Task")
    assert result == True
    print("✅ update_todo() works")

    # Test complete_todo
    result = service.complete_todo(1)
    assert result == True
    todos, completed, pending = service.list_todos()
    assert completed == 1
    print("✅ complete_todo() works")

    # Test delete_todo
    result = service.delete_todo(1)
    assert result == True
    assert len(service.list_todos()[0]) == 1
    print("✅ delete_todo() works")

def test_validations():
    """Test Input Validations"""
    print("\n=== Testing Input Validations ===")

    storage = TodoStorage()

    # Test empty title
    try:
        storage.add("")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
        print("✅ Empty title validation works")

    # Test title too long
    try:
        storage.add("x" * 201)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "200" in str(e)
        print("✅ Title length validation works")

    # Test description too long
    try:
        storage.add("Valid title", "x" * 1001)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "1000" in str(e)
        print("✅ Description length validation works")

def test_performance():
    """Test Performance Requirements"""
    print("\n=== Testing Performance ===")

    storage = TodoStorage()
    service = TodoService(storage)

    # Test startup time (should be < 1s)
    start = time.time()
    service2 = TodoService(TodoStorage())
    startup_time = time.time() - start
    assert startup_time < 1.0
    print(f"✅ Startup time: {startup_time:.4f}s (< 1s)")

    # Test add task performance (should be < 500ms)
    start = time.time()
    service.create_todo("Performance Test Task")
    add_time = (time.time() - start) * 1000
    assert add_time < 500
    print(f"✅ Add task time: {add_time:.2f}ms (< 500ms)")

    # Test view 100 items (should be < 1s)
    for i in range(100):
        service.create_todo(f"Task {i}")

    start = time.time()
    todos, completed, pending = service.list_todos()
    view_time = time.time() - start
    assert view_time < 1.0
    assert len(todos) == 101  # 100 + 1 from before
    print(f"✅ View 101 items time: {view_time:.4f}s (< 1s)")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Console Todo App - Automated Test Suite")
    print("=" * 50)

    try:
        test_model_layer()
        test_storage_layer()
        test_service_layer()
        test_validations()
        test_performance()

        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\n📊 Test Summary:")
        print("  - Model Layer: ✅")
        print("  - Storage Layer: ✅")
        print("  - Service Layer: ✅")
        print("  - Validations: ✅")
        print("  - Performance: ✅")
        print("\n🚀 Application is ready for use!")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
