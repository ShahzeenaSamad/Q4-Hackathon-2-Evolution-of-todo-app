# Feature: Task CRUD Operations

## Feature Overview

Implement complete Create, Read, Update, and Delete (CRUD) functionality for tasks in the web application, building upon the Phase I console app features.

---

## User Stories

### Create Task
**As a** user
**I can** create a new task with a title and optional description
**So that** I can track my to-do items

### View Tasks
**As a** user
**I can** view all my tasks in a list
**So that** I can see what I need to do

### Update Task
**As a** user
**I can** update a task's title and description
**So that** I can modify my plans

### Delete Task
**As a** user
**I can** delete a task I no longer need
**So that** I can keep my list clean

### Complete Task
**As a** user
**I can** mark a task as completed or incomplete
**So that** I can track my progress

---

## Functional Requirements

### FR-1: Create Task

**Description:** Users can create new tasks with a title and optional description.

**Input Fields:**
- `title` (string, required, 1-200 characters)
- `description` (string, optional, max 1000 characters)

**Validation Rules:**
- Title cannot be empty
- Title must be 1-200 characters
- Description must be 0-1000 characters
- HTML tags are stripped from inputs

**Business Rules:**
- Task is automatically assigned to the authenticated user
- Task `completed` status defaults to `false`
- Task `created_at` timestamp is automatically set
- Task `updated_at` timestamp is automatically set

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-17T10:30:00Z",
    "updated_at": "2026-01-17T10:30:00Z"
  }
}
```

**Error Responses:**
```json
// Missing title
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required"
  }
}

// Title too long
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title must be 200 characters or less"
  }
}
```

---

### FR-2: View Tasks (List)

**Description:** Users can view all their tasks in a paginated list.

**Query Parameters:**
- `page` (integer, optional, default: 1)
- `limit` (integer, optional, default: 20, max: 100)
- `status` (string, optional: "all" | "pending" | "completed", default: "all")
- `sort` (string, optional: "created" | "title" | "updated", default: "created")

**Response Format:**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "created_at": "2026-01-17T10:30:00Z",
        "updated_at": "2026-01-17T10:30:00Z"
      },
      {
        "id": 2,
        "title": "Call mom",
        "description": null,
        "completed": true,
        "created_at": "2026-01-16T15:20:00Z",
        "updated_at": "2026-01-17T09:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 2,
      "totalPages": 1
    }
  }
}
```

**Business Rules:**
- Only tasks belonging to the authenticated user are returned
- Tasks are sorted according to the `sort` parameter
- Pagination must be enforced (default 20 per page)
- Empty list returns `{"tasks": [], "pagination": {...}}`

---

### FR-3: View Single Task

**Description:** Users can view details of a specific task.

**URL Parameter:**
- `id` (integer, required) - Task ID

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-17T10:30:00Z",
    "updated_at": "2026-01-17T10:30:00Z"
  }
}
```

**Error Responses:**
```json
// Task not found
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}

// Task belongs to different user
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied"
  }
}
```

**Business Rules:**
- User can only view their own tasks
- 404 returned if task doesn't exist
- 403 returned if task belongs to different user

---

### FR-4: Update Task

**Description:** Users can update a task's title and/or description.

**URL Parameter:**
- `id` (integer, required) - Task ID

**Request Body:**
```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas"
}
```

**Validation Rules:**
- Same as FR-1 (Create Task)
- At least one field must be provided

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries and fruits",
    "description": "Milk, eggs, bread, apples, bananas",
    "completed": false,
    "created_at": "2026-01-17T10:30:00Z",
    "updated_at": "2026-01-17T11:00:00Z"
  }
}
```

**Business Rules:**
- User can only update their own tasks
- `updated_at` timestamp is automatically updated
- Partial updates allowed (only provided fields are updated)

---

### FR-5: Delete Task

**Description:** Users can permanently delete a task.

**URL Parameter:**
- `id` (integer, required) - Task ID

**Success Response:**
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

**Error Responses:**
```json
// Task not found
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}

// Task belongs to different user
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied"
  }
}
```

**Business Rules:**
- User can only delete their own tasks
- Deletion is permanent (no soft delete)
- 404 returned if task doesn't exist
- 403 returned if task belongs to different user

---

### FR-6: Toggle Task Completion

**Description:** Users can mark a task as completed or incomplete.

**URL Parameter:**
- `id` (integer, required) - Task ID

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2026-01-17T10:30:00Z",
    "updated_at": "2026-01-17T11:00:00Z"
  }
}
```

**Business Rules:**
- Toggles between `true` and `false`
- User can only toggle their own tasks
- `updated_at` timestamp is automatically updated

---

## Non-Functional Requirements

### NFR-1: Performance
- **List Tasks:** < 300ms (p95) for up to 100 tasks
- **Create Task:** < 200ms (p95)
- **Update Task:** < 200ms (p95)
- **Delete Task:** < 200ms (p95)

### NFR-2: Security
- All endpoints require valid JWT token
- User can only access their own tasks
- SQL injection prevention via parameterized queries
- XSS prevention via input sanitization

### NFR-3: Scalability
- Support pagination for large task lists
- Database queries must use indexes
- Connection pooling for database access

### NFR-4: Usability
- Clear error messages
- User-friendly validation feedback
- Responsive UI on mobile and desktop

---

## UI Requirements

### Task List Component

**Location:** `@specs/ui/components.md#task-list`

**Features:**
- Display tasks in card or list format
- Show task title, description preview, status
- Visual indication of completion (checkbox, strikethrough)
- Quick actions: Edit, Delete, Toggle Complete
- Empty state when no tasks exist
- Loading state during data fetch
- Error state with retry option

### Task Form Component

**Location:** `@specs/ui/components.md#task-form`

**Features:**
- Title input (required)
- Description textarea (optional)
- Character counter for both fields
- Real-time validation
- Submit and cancel buttons
- Loading state during submission
- Success/error feedback

### Task Detail Component

**Location:** `@specs/ui/components.md#task-detail`

**Features:**
- Display full task information
- Edit button to modify task
- Delete button with confirmation
- Back button to return to list
- Timestamp display (created, updated)

---

## API Endpoints

**Detailed Specification:** `@specs/api/rest-endpoints.md`

**Summary:**
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/tasks` | List all user's tasks |
| POST | `/api/v1/tasks` | Create new task |
| GET | `/api/v1/tasks/{id}` | Get task details |
| PUT | `/api/v1/tasks/{id}` | Update task |
| DELETE | `/api/v1/tasks/{id}` | Delete task |
| PATCH | `/api/v1/tasks/{id}/complete` | Toggle completion |

---

## Database Schema

**Detailed Specification:** `@specs/database/schema.md`

**Table Structure:**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

---

## Acceptance Criteria

### AC-1: Create Task
- ✅ User can create task with valid title
- ✅ System rejects empty title
- ✅ System rejects title > 200 characters
- ✅ System accepts optional description
- ✅ System rejects description > 1000 characters
- ✅ Task is assigned to authenticated user
- ✅ Response includes all task fields

### AC-2: View Tasks
- ✅ User sees only their own tasks
- ✅ List is paginated (default 20 per page)
- ✅ User can filter by status (all/pending/completed)
- ✅ User can sort by created/title/updated
- ✅ Empty list handled gracefully

### AC-3: View Single Task
- ✅ User can view their own task
- ✅ 404 for non-existent task
- ✅ 403 for other user's task

### AC-4: Update Task
- ✅ User can update their own task
- ✅ At least one field required
- ✅ Validation rules apply
- ✅ 404 for non-existent task
- ✅ 403 for other user's task
- ✅ `updated_at` timestamp updates

### AC-5: Delete Task
- ✅ User can delete their own task
- ✅ 404 for non-existent task
- ✅ 403 for other user's task
- ✅ Deletion is permanent

### AC-6: Toggle Completion
- ✅ User can toggle their own task
- ✅ Status flips between true/false
- ✅ 404 for non-existent task
- ✅ 403 for other user's task
- ✅ `updated_at` timestamp updates

---

## Edge Cases

### EC-1: Concurrent Updates
**Scenario:** User updates task from two devices simultaneously
**Handling:** Last write wins (based on `updated_at`)

### EC-2: Deleted Task Access
**Scenario:** User tries to access deleted task
**Handling:** Return 404 NOT_FOUND

### EC-3: Pagination Edge
**Scenario:** User requests page beyond available
**Handling:** Return empty array with valid pagination info

### EC-4: Special Characters
**Scenario:** User enters emoji or special characters in title
**Handling:** Accept and store as-is (UTF-8 support)

### EC-5: Very Long Description
**Scenario:** User enters 1000+ character description
**Handling:** Reject with validation error

---

## Testing Requirements

### Unit Tests
- ✅ Task model validation
- ✅ Title length validation
- ✅ Description length validation
- ✅ User ownership checks

### Integration Tests
- ✅ Create task endpoint
- ✅ List tasks endpoint with filters
- ✅ Update task endpoint
- ✅ Delete task endpoint
- ✅ Toggle completion endpoint
- ✅ Error handling (404, 403, 401)

### E2E Tests
- ✅ Create task from UI
- ✅ View task list
- ✅ Update task from UI
- ✅ Delete task from UI
- ✅ Toggle completion from UI

---

## Related Specifications

- **Overview:** `@specs/overview.md`
- **Architecture:** `@specs/architecture.md`
- **API:** `@specs/api/rest-endpoints.md`
- **Database:** `@specs/database/schema.md`
- **UI:** `@specs/ui/components.md`
- **Authentication:** `@specs/features/authentication.md`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
