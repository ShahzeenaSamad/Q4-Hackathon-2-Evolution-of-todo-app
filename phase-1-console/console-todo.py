#!/usr/bin/env python3
"""
Console Todo App - Phase I Implementation
A simple command-line todo application with in-memory storage.

Author: Hackathon II Participant
Created: January 16, 2026
Python: 3.13+
"""

from datetime import datetime
from typing import List, Optional
import sys


# =============================================================================
# MODEL LAYER
# =============================================================================

class Todo:
    """Represents a single todo item."""

    def __init__(self, todo_id: int, title: str, description: str = "") -> None:
        """Initialize a Todo object.

        Args:
            todo_id: Unique sequential identifier
            title: Task title (1-200 characters)
            description: Optional task description
        """
        self.id = todo_id
        self.title = title.strip()
        self.description = description.strip()
        self.completed = False
        self.created_at = datetime.now().isoformat()

    def mark_completed(self) -> None:
        """Mark the todo as completed."""
        self.completed = True

    def mark_pending(self) -> None:
        """Mark the todo as pending."""
        self.completed = False

    def to_dict(self) -> dict:
        """Convert todo to dictionary.

        Returns:
            Dictionary representation of todo
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at
        }

    def __repr__(self) -> str:
        """String representation of todo."""
        status = "[v]" if self.completed else " "
        return f"[{self.id}] {status} {self.title}"


class TodoStorage:
    """In-memory storage for todos."""

    def __init__(self) -> None:
        """Initialize empty storage."""
        self.todos: List[Todo] = []
        self.next_id: int = 1

    def add(self, title: str, description: str = "") -> Todo:
        """Add a new todo to storage.

        Args:
            title: Task title
            description: Optional description

        Returns:
            Created Todo object
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")

        if description and len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

        todo = Todo(self.next_id, title, description)
        self.todos.append(todo)
        self.next_id += 1
        return todo

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Retrieve todo by ID.

        Args:
            todo_id: Task identifier

        Returns:
            Todo object if found, None otherwise
        """
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def get_all(self) -> List[Todo]:
        """Get all todos.

        Returns:
            List of all Todo objects
        """
        return self.todos.copy()

    def update(self, todo_id: int, title: str = None,
              description: str = None) -> bool:
        """Update todo by ID.

        Args:
            todo_id: Task identifier
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if updated, False if not found
        """
        todo = self.get_by_id(todo_id)
        if not todo:
            return False

        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            if len(title) > 200:
                raise ValueError("Title must be 200 characters or less")
            todo.title = title.strip()

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less")
            todo.description = description.strip()

        return True

    def delete(self, todo_id: int) -> bool:
        """Delete todo by ID.

        Args:
            todo_id: Task identifier

        Returns:
            True if deleted, False if not found
        """
        todo = self.get_by_id(todo_id)
        if not todo:
            return False
        self.todos.remove(todo)
        return True

    def get_completed_count(self) -> int:
        """Count completed todos.

        Returns:
            Number of completed tasks
        """
        return sum(1 for todo in self.todos if todo.completed)

    def get_pending_count(self) -> int:
        """Count pending todos.

        Returns:
            Number of pending tasks
        """
        return sum(1 for todo in self.todos if not todo.completed)

    def is_empty(self) -> bool:
        """Check if storage is empty.

        Returns:
            True if no todos, False otherwise
        """
        return len(self.todos) == 0


# =============================================================================
# SERVICE LAYER
# =============================================================================

class TodoService:
    """Business logic for todo operations."""

    def __init__(self, storage: TodoStorage) -> None:
        """Initialize service with storage.

        Args:
            storage: TodoStorage instance
        """
        self.storage = storage

    def create_todo(self, title: str, description: str = "") -> Todo:
        """Create a new todo.

        Args:
            title: Task title
            description: Optional description

        Returns:
            Created Todo object
        """
        return self.storage.add(title, description)

    def list_todos(self) -> tuple[List[Todo], int, int]:
        """Get all todos with statistics.

        Returns:
            Tuple of (todos list, completed count, pending count)
        """
        todos = self.storage.get_all()
        completed = self.storage.get_completed_count()
        pending = self.storage.get_pending_count()
        return todos, completed, pending

    def update_todo(self, todo_id: int, title: str = None) -> bool:
        """Update todo title.

        Args:
            todo_id: Task identifier
            title: New title

        Returns:
            True if updated, False if not found
        """
        if not title:
            return False
        return self.storage.update(todo_id, title=title)

    def complete_todo(self, todo_id: int) -> bool:
        """Mark todo as completed.

        Args:
            todo_id: Task identifier

        Returns:
            True if marked completed, False if not found
        """
        todo = self.storage.get_by_id(todo_id)
        if not todo:
            return False
        todo.mark_completed()
        return True

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo.

        Args:
            todo_id: Task identifier

        Returns:
            True if deleted, False if not found
        """
        return self.storage.delete(todo_id)


# =============================================================================
# CLI INTERFACE
# =============================================================================

class TodoCLI:
    """Command-line interface for todo app."""

    def __init__(self, service: TodoService) -> None:
        """Initialize CLI with service.

        Args:
            service: TodoService instance
        """
        self.service = service

    def display_menu(self) -> None:
        """Display main menu."""
        print("\n" + "=" * 40)
        print("Welcome to Todo App")
        print("=" * 40)
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo")
        print("4. Complete Todo")
        print("5. Delete Todo")
        print("6. Exit")
        print("=" * 40)

    def display_todos(self, todos: List[Todo], completed: int, pending: int) -> None:
        """Display all todos.

        Args:
            todos: List of Todo objects
            completed: Number of completed tasks
            pending: Number of pending tasks
        """
        if not todos:
            print("\n📝 No tasks yet. Add your first task!")
            return

        print("\nYour Tasks:")
        print("-" * 40)
        for todo in todos:
            print(todo)
        print("-" * 40)
        print(f"\nTotal tasks: {len(todos)} ({completed} completed, {pending} pending)")

    def get_choice(self) -> int:
        """Get and validate user menu choice.

        Returns:
            Validated menu choice (1-6)
        """
        while True:
            try:
                choice = input("\nEnter your choice (1-6): ").strip()
                choice_int = int(choice)
                if 1 <= choice_int <= 6:
                    return choice_int
                print("❌ Please enter a number between 1 and 6")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

    def prompt_add_todo(self) -> tuple[str, str]:
        """Prompt user for todo details.

        Returns:
            Tuple of (title, description)
        """
        print("\n--- Add New Todo ---")

        while True:
            title = input("Title: ").strip()
            if title:
                break
            print("❌ Title cannot be empty. Please try again.")

        description = input("Description (optional, press Enter to skip): ").strip()

        return title, description

    def prompt_update_todo(self) -> Optional[int]:
        """Prompt user for todo ID and new title.

        Returns:
            Todo ID if valid, None otherwise
        """
        print("\n--- Update Todo ---")

        todo_id = self._get_todo_id()
        if todo_id is None:
            return None

        new_title = input(f"New title: ").strip()
        if not new_title:
            print("❌ Title cannot be empty")
            return None

        return todo_id

    def prompt_complete_todo(self) -> Optional[int]:
        """Prompt user for todo ID to mark complete.

        Returns:
            Todo ID if valid, None otherwise
        """
        print("\n--- Complete Todo ---")
        return self._get_todo_id()

    def prompt_delete_todo(self) -> Optional[int]:
        """Prompt user for todo ID to delete.

        Returns:
            Todo ID if valid, None otherwise
        """
        print("\n--- Delete Todo ---")
        return self._get_todo_id()

    def _get_todo_id(self) -> Optional[int]:
        """Helper to get validated todo ID.

        Returns:
            Validated todo ID or None
        """
        while True:
            try:
                id_str = input("Enter task ID: ").strip()
                if not id_str:
                    print("❌ Task ID cannot be empty")
                    return None

                todo_id = int(id_str)
                if todo_id <= 0:
                    print("❌ Task ID must be positive")
                    continue

                # Check if task exists
                if not self.service.storage.get_by_id(todo_id):
                    print(f"❌ Task {todo_id} not found")
                    return None

                return todo_id
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

    def show_success(self, message: str) -> None:
        """Display success message.

        Args:
            message: Success message
        """
        print(f"✅ {message}")

    def show_error(self, message: str) -> None:
        """Display error message.

        Args:
            message: Error message
        """
        print(f"❌ {message}")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main() -> None:
    """Main application entry point."""
    # Initialize layers
    storage = TodoStorage()
    service = TodoService(storage)
    cli = TodoCLI(service)


    # Main application loop
    while True:
        try:
            cli.display_menu()
            choice = cli.get_choice()

            if choice == 1:
                # Add Todo
                title, description = cli.prompt_add_todo()
                todo = service.create_todo(title, description)
                cli.show_success(f"Task added: {todo}")

            elif choice == 2:
                # View Todos
                todos, completed, pending = service.list_todos()
                cli.display_todos(todos, completed, pending)

            elif choice == 3:
                # Update Todo
                if service.storage.is_empty():
                    cli.show_error("No tasks to update. Add a task first.")
                    continue

                todo_id = cli.prompt_update_todo()
                if todo_id is not None:
                    new_title = input(f"New title: ").strip()
                    if not new_title:
                        cli.show_error("Title cannot be empty")
                        continue

                    if service.update_todo(todo_id, new_title):
                        cli.show_success(f"Task {todo_id} updated")
                    else:
                        cli.show_error(f"Failed to update task {todo_id}")

            elif choice == 4:
                # Complete Todo
                if service.storage.is_empty():
                    cli.show_error("No tasks to complete. Add a task first.")
                    continue

                todo_id = cli.prompt_complete_todo()
                if todo_id is not None:
                    if service.complete_todo(todo_id):
                        cli.show_success(f"Task {todo_id} marked as complete")
                    else:
                        cli.show_error(f"Failed to complete task {todo_id}")

            elif choice == 5:
                # Delete Todo
                if service.storage.is_empty():
                    cli.show_error("No tasks to delete. Add a task first.")
                    continue

                todo_id = cli.prompt_delete_todo()
                if todo_id is not None:
                    if service.delete_todo(todo_id):
                        cli.show_success(f"Task {todo_id} deleted")
                    else:
                        cli.show_error(f"Failed to delete task {todo_id}")

            elif choice == 6:
                # Exit
                print("\n👋 Thank you for using Todo App!")
                print("💾 Remember: Your tasks are saved in memory only")
                print("    (Consider implementing file/database storage in Phase II)")
                print("\nGoodbye! 👋\n")
                break

        except KeyboardInterrupt:
            print("\n\n\n🛑 Interrupted by user")
            print("👋 Goodbye! 👋\n")
            sys.exit(0)
        except Exception as e:
            cli.show_error(f"An error occurred: {str(e)}")
            print("Please try again or contact support.\n")


if __name__ == "__main__":
    main()
