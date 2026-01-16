# Specification: Console Todo App (Phase I)

**Feature**: Console Todo Application
**Phase**: Phase I
**Created**: January 16, 2026
**Project**: Hackathon II - Evolution of Todo
**Spec Reference**: @specs/features/phase1-console-crud.md

---

## Overview

**Feature**: Command-line todo application for daily task management

**Vision**: Simple, in-memory todo list with menu-driven interface

**Goal**: Demonstrate spec-driven development while building essential CRUD skills

---

## User Scenarios

### User Story 1: Create and Manage Tasks (Priority: P1)

**Scenario**: User wants to add tasks, view list, update, complete and delete tasks in a console app

**User Stories**:
- As a user, I want to add a new task so that I can remember important things
- As a user, I want to view all my tasks so I can see what I need to do
- As a user, I want to update a task title so I can correct mistakes
- As a user, I want to mark tasks as completed so I can track progress
- As a user, I want to delete tasks I no longer need

---

## Requirements

### Functional Requirements

- **FR-001**: Display menu with 6 options when app starts (Add, View, Update, Complete, Delete, Exit)
- **FR-002: System MUST accept user choice and route to appropriate action
- **FR-003**: System MUST allow adding task with title (required) and optional description
- **FR-004**: System MUST assign unique sequential ID to each task starting from 1
- **FR-005**: System MUST store all tasks in memory (list) without persistence
- **FR-006**: System MUST display all tasks with ID, title, completion status
- **FR-007**: System MUST allow updating task title by ID
- **FR-008**: System MUST allow marking task as completed/incomplete by ID
- **FR-009**: System MUST allow deleting task by ID
- **FRR-010**: System MUST validate task ID exists before update/delete/complete operations
- **FR-011**: System MUST trim whitespace from inputs
- **FR-012**: System MUST handle empty titles with error message
- **FR-013**: System MUST exit cleanly with goodbye message

---

## Acceptance Criteria

### Test Cases

**TC-001**: App starts and shows menu
- Input: `python console-todo.py`
- Expected: Welcome message + menu with 6 options

**TC-002: Add task
- Input: Menu choice "1"
- Input: Title: "Buy groceries"
- Input: Description: (optional)
- Expected: Task added successfully

**TC-003**: View tasks
- Input: Menu choice "2"
- Expected: List of all tasks with IDs

**TC-004**: Update task
- Input: Menu choice "3"
- Input: Task ID: 1
- Input: New title: "Updated title"
- Expected: Task updated successfully

**TC-005**: Complete task
- Input: Menu choice "4"
- Input: Task ID: 1
- Expected: Task marked as complete

**TC-006**: Delete task
- Input: Menu choice "5"
- Input: Task ID: 1
- Expected: Task deleted successfully

**TC-007: Exit application
- Input: Menu choice "6"
- Expected: Clean exit with goodbye message

---

## Data Model

### Todo Entity

```
Todo {
    id: int              # Unique sequential ID
    title: str           # Title (1-200 chars, required)
    description: str     # Description (optional, max 1000 chars)
    completed: bool      # Completion status
    created_at: str      # ISO timestamp
}
```

### Storage

```
TodoStorage {
    todos: List<Todo>     # In-memory list
    next_id: int          # Next available ID
}
```

---

## Scope

### In Scope
- Single file Python console application
- In-memory storage
- Menu-driven interface
- 5 menu options: Add, View, Update, Complete, Delete, Exit
- Input validation
- Error handling
- PEP 8 compliance

### Out of Scope
- File/database persistence
- User authentication
- Multiple users
- Advanced features (search, filter, priorities)
- GUI interface
- Web interface

---

## Constraints

- **Language**: Python 3.13+ only
- **Dependencies**: Standard library only
- **Architecture**: Single monolithic file
- **Storage**: In-memory only
- **Interface**: Command-line only

---

## Success Criteria

- **SC-001**: App starts in under 1 second
- **SC-002: Add task operation completes in under 500ms
- **SC-003**: View 100 tasks in under 1 second
- **SC-004**: All 5 menu options work correctly
- **SC-005**: No crashes on invalid input
- **SC-006**: PEP 8 compliant code
- **SC-007**: All functions have docstrings
- **SC-008**: Runs on Python 3.13+

---

**Ready for Planning**: ✅
**Next**: Create implementation plan
