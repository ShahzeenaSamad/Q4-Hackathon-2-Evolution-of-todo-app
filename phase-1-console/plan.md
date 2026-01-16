# Implementation Plan: Console Todo App (Phase I)

**Feature**: Console Todo Application
**Phase**: Phase I
**Created**: January 16, 2026
**Spec Reference**: spec.md, @specs/features/phase1-console-crud.md

---

## Architecture Overview

**Single File Architecture**:
```
console-todo.py (519 lines)
├── Model Layer
│   ├── Todo class
│   └── TodoStorage class
├── Service Layer
│   └── TodoService class
├── Interface Layer
│   └── TodoCLI class
└── Main
    └── main() function
```

---

## Component Details

### **1. Todo Class** (Model Layer)

**Purpose**: Represents a single todo item

**Attributes**:
- `id: int` - Unique sequential identifier
- `title: str` - Task title (1-200 chars)
- `description: str` - Optional description (max 1000 chars)
- `completed: bool` - Completion status
- `created_at: str` - ISO timestamp

**Methods**:
- `mark_completed()` - Mark as done
- `mark_pending()` - Mark as pending
- `to_dict()` - Convert to dictionary
- `__repr__()` - String representation

---

### **2. TodoStorage Class** (Model Layer)

**Purpose**: In-memory storage manager

**Attributes**:
- `todos: List[Todo]` - List of Todo objects
- `next_id: int` - Next ID to assign

**Methods**:
- `add(title, description)` - Create new todo
- `get_by_id(id)` - Find todo by ID
- `get_all()` - Get all todos
- `update(id, title, description)` - Update todo
- `delete(id)` - Remove todo
- `get_completed_count()` - Count completed todos
- `get_pending_count()` - Count pending todos
- `is_empty()` - Check if storage is empty

---

### **3. TodoService Class** (Service Layer)

**Purpose**: Business logic layer

**Methods**:
- `create_todo(title, description)` - Create with validation
- `list_todos()` - Get all with statistics
- `update_todo(id, title)` - Update existing todo
- `complete_todo(id)` - Mark as complete
- `delete_todo(id)` - Delete todo

---

### **4. TodoCLI Class** (Interface Layer)

**Purpose**: Command-line interface

**Methods**:
- `display_menu()` - Show menu options
- `display_todos(todos, completed, pending)` - Display formatted list
- `get_choice()` - Get validated user choice
- `prompt_add_todo()` - Get user input for adding
- `prompt_update_todo()` - Get input for updating
- `prompt_complete_todo()` - Get task ID to complete
- `prompt_delete_todo()` - Get task ID to delete
- `show_success(message)` - Show success message
- `show_error(message)` - Show error message

---

### **5. main() Function** (Entry Point)

**Purpose**: Application bootstrap and main loop

**Flow**:
1. Initialize Storage
2. Initialize Service
3. Initialize CLI
4. Show welcome message
5. Main application loop:
   - Display menu
   - Get choice
   - Execute action based on choice
   - Handle errors
   - Repeat until Exit
6. Exit with goodbye message

---

## Implementation Checklist

### Model Layer (✅ Complete)

- [x] Create Todo class with attributes
- [x] Add Todo.mark_completed() method
- [x] Add Todo.mark_pending() method
- [x] Add Todo.to_dict() method
- [x] Add Todo.__repr__() method

### Storage Layer (✅ Complete)

- [x] Create TodoStorage class
- [x] Implement TodoStorage.add()
- [x] Implement TodoStorage.get_by_id()
- [x] Implement TodoStorage.get_all()
- [x] Implement TodoStorage.update()
- [x] Implement TodoStorage.delete()
- [x] Implement TodoStorage.get_completed_count()
- [x] Implement TodoStorage.get_pending_count()
- [x] Implement TodoStorage.is_empty()

### Service Layer (✅ Complete)

- [x] Create TodoService class
- [x] Implement TodoService.create_todo()
- [x] Implement TodoService.list_todos()
- [x] Implement TodoService.update_todo()
- [x] Implement TodoService.complete_todo()
- [x] Implement TodoService.delete_todo()

### CLI Layer (✅ Complete)

- [x] Create TodoCLI class
- [x] Implement TodoCLI.display_menu()
- [x] Implement TodoCLI.display_todos()
- [x] Implement TodoCLI.get_choice()
- [x] Implement TodoCLI.prompt_add_todo()
- [x] Implement TodoCLI.prompt_update_todo()
- [x] Implement TodoCLI.prompt_complete_todo()
- [x] Implement TodoCLI.prompt_delete_todo()
- [x] Implement TodoCLI.show_success()
- [x] Implement TodoCLI.show_error()

### Main Application (✅ Complete)

- [x] Implement main() function
- [x] Add welcome message
- [x] Add exit message with data loss warning
- [x] Add KeyboardInterrupt handler
- [x] Add generic exception handler
- [x] Implement all 6 menu choices

---

## Error Handling

### Input Validation

- **Empty Title**: Show error "Title cannot be empty"
- **Invalid ID**: Show error "Task {id} not found"
- **Non-numeric ID**: Show error "Invalid input. Please enter a number"
- **Negative ID**: Show error "Task ID must be positive"
- **Empty List**: Show message "No tasks yet. Add your first task!"

### Graceful Degradation

- **Empty Title**: Prompt again, don't crash
- **Invalid Input**: Show error, prompt again, don't crash
- **Ctrl+C**: Clean exit with friendly message
- **Generic Errors**: Show error, suggest trying again

---

## Code Quality Standards

### PEP 8 Compliance

- Line length: 79 characters max
- Indentation: 4 spaces
- Naming: snake_case for variables, PascalCase for classes
- Imports: Standard library only
- Docstrings: Google style

### Type Hints

- All functions have type hints
- Use Optional[T] for nullable returns
- Use List, Dict, Tuple as needed

### Documentation

- Google style docstrings
- All classes documented
- All methods documented
- Complex logic explained

---

## Quick Start

```bash
cd phase-1-console
python console-todo.py
```

---

## Success Criteria Validation

| Criterion | Test Method | Target |
|-----------|-------------|--------|
| SC-001: App starts < 1s | Run app, time startup | < 1s |
| SC-002: Add < 500ms | Add task and time operation | < 500ms |
| ✅ SC-003: View 100 items < 1s | Add 100 tasks, time view | < 1s |
| ✅ SC-004: All 6 options work | Test each option | All work |
| ✅ SC-005: No crashes on bad input | Test invalid inputs | Graceful |
| ✅ SC-006: PEP 8 | Run pylint | Pass |
| ✅ SC-007: Docstrings present | Check all functions | Present |
| ✅ SC-008: Runs on Python 3.13+ | Run with python3 | ✅ Works |

---

## Implementation Status

- [x] Code complete: `console-todo.py` (519 lines)
- [x] Model layer: Todo, TodoStorage implemented
- [x] Service layer: TodoService implemented
- [x] CLI layer: TodoCLI implemented
- [x] Main application: main() implemented
- [x] Error handling: All errors handled
- [x] Validation: All inputs validated

---

## Next Steps

1. ✅ **Planning Complete**
2. ✅ **Implementation Complete**
3. ⏳ **Testing Phase**: Manual user testing required
4. ⏳ **Phase II** (Future): Full-Stack Web App

---

**Status**: ✅ **READY FOR TESTING**
**Run Command**: `python phase-1-console/console-todo.py`
