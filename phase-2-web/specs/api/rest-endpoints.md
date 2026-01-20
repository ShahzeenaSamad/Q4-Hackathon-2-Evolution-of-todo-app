# REST API Endpoints Specification

## API Overview

This document defines the complete REST API contract for Phase II of the Todo App.

---

## Base Information

**Base URL:**
- Development: `http://localhost:8000`
- Production: `https://your-backend-api.com`

**API Prefix:** `/api/v1`

**Content-Type:** `application/json`

**Authentication:** JWT Token (Bearer)

---

## Authentication

### Token Format

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

### Token Payload

```json
{
  "sub": "user_123abc",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1737106200,
  "exp": 1737711000
}
```

---

## Response Format

### Success Response

```json
{
  "success": true,
  "data": {
    // Response data here
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}  // Optional additional details
  }
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Access denied to resource |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Authentication Endpoints

### POST /api/v1/auth/signup

Create a new user account.

**Authentication:** Not Required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"  // Optional
}
```

**Validation:**
- `email`: Required, valid email format, unique
- `password`: Required, min 8 characters
- `name`: Optional, max 100 characters

**Success Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123abc",
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2026-01-17T10:30:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**

**400 Bad Request (Invalid Email):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format"
  }
}
```

**400 Bad Request (Password Too Short):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Password must be at least 8 characters"
  }
}
```

**409 Conflict (Email Exists):**
```json
{
  "success": false,
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "An account with this email already exists"
  }
}
```

---

### POST /api/v1/auth/login

Authenticate a user and receive JWT token.

**Authentication:** Not Required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123abc",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**

**401 Unauthorized (Invalid Credentials):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

**404 Not Found (User Not Found):**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "No account found with this email"
  }
}
```

---

### POST /api/v1/auth/logout

Logout current user (invalidate session).

**Authentication:** Required

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Logged out successfully"
  }
}
```

---

### GET /api/v1/auth/me

Get current authenticated user's information.

**Authentication:** Required

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123abc",
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2026-01-17T10:30:00Z"
    }
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

---

## Task Endpoints

### GET /api/v1/tasks

List all tasks for the authenticated user.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `limit` | integer | 20 | Items per page (max 100) |
| `status` | string | "all" | Filter: "all", "pending", "completed" |
| `sort` | string | "created" | Sort: "created", "title", "updated" |

**Example Request:**
```
GET /api/v1/tasks?page=1&limit=20&status=pending&sort=created
```

**Success Response (200):**
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

**Empty List Response (200):**
```json
{
  "success": true,
  "data": {
    "tasks": [],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 0,
      "totalPages": 0
    }
  }
}
```

---

### POST /api/v1/tasks

Create a new task.

**Authentication:** Required

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation:**
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

**Success Response (201):**
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

**400 Bad Request (Missing Title):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required"
  }
}
```

**400 Bad Request (Title Too Long):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title must be 200 characters or less"
  }
}
```

---

### GET /api/v1/tasks/{id}

Get a specific task by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer, required) - Task ID

**Example Request:**
```
GET /api/v1/tasks/1
```

**Success Response (200):**
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

**404 Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}
```

**403 Forbidden (Other User's Task):**
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied"
  }
}
```

---

### PUT /api/v1/tasks/{id}

Update a task.

**Authentication:** Required

**URL Parameters:**
- `id` (integer, required) - Task ID

**Request Body:**
```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples"
}
```

**Validation:** Same as POST /api/v1/tasks

At least one field must be provided.

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries and fruits",
    "description": "Milk, eggs, bread, apples",
    "completed": false,
    "created_at": "2026-01-17T10:30:00Z",
    "updated_at": "2026-01-17T11:00:00Z"
  }
}
```

**Error Responses:** Same as GET /api/v1/tasks/{id}

---

### DELETE /api/v1/tasks/{id}

Delete a task.

**Authentication:** Required

**URL Parameters:**
- `id` (integer, required) - Task ID

**Example Request:**
```
DELETE /api/v1/tasks/1
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

**Error Responses:** Same as GET /api/v1/tasks/{id}

---

### PATCH /api/v1/tasks/{id}/complete

Toggle task completion status.

**Authentication:** Required

**URL Parameters:**
- `id` (integer, required) - Task ID

**Request Body:**
Empty (no body required)

**Success Response (200):**
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

**Error Responses:** Same as GET /api/v1/tasks/{id}

---

## Health Check

### GET /api/v1/health

Check API and database health status.

**Authentication:** Not Required

**Success Response (200):**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-17T10:30:00Z"
}
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `UNAUTHORIZED` | 401 | Authentication required or failed |
| `FORBIDDEN` | 403 | Access denied to resource |
| `NOT_FOUND` | 404 | Resource not found |
| `EMAIL_EXISTS` | 409 | Email already registered |
| `INVALID_CREDENTIALS` | 401 | Invalid login credentials |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Rate Limiting

**Current Phase:** Not implemented (future enhancement)

**Recommended:**
- 100 requests per minute per user
- 1000 requests per hour per user

**Rate Limit Headers (Future):**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1737106800
```

---

## CORS Configuration

**Allowed Origins:**
- Development: `http://localhost:3000`
- Production: `https://your-frontend.vercel.app`

**Allowed Methods:**
- GET, POST, PUT, PATCH, DELETE, OPTIONS

**Allowed Headers:**
- Content-Type, Authorization

**Credentials:**
- Supported (for cookies)

---

## OpenAPI Documentation

**Swagger UI:** `/docs`
**ReDoc:** `/redoc`
**OpenAPI JSON:** `/openapi.json`

**Auto-generated by FastAPI**

---

## Testing Examples

### cURL Examples

**Signup:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123",
    "name": "John Doe"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'
```

**Get Tasks:**
```bash
curl -X GET http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Create Task:**
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

---

## Frontend API Client

**Detailed Specification:** `@specs/ui/components.md#api-client`

**Basic Implementation:**
```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
  }

  async request(endpoint: string, options?: RequestInit) {
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { 'Authorization': `Bearer ${this.token}` })
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error.message);
    }

    return response.json();
  }

  // Auth methods
  async signup(data: SignupData) {
    return this.request('/api/v1/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async login(data: LoginData) {
    return this.request('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Task methods
  async getTasks(params?: TaskParams) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/api/v1/tasks?${qs}`);
  }

  async createTask(data: CreateTaskData) {
    return this.request('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async updateTask(id: number, data: UpdateTaskData) {
    return this.request(`/api/v1/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async deleteTask(id: number) {
    return this.request(`/api/v1/tasks/${id}`, {
      method: 'DELETE'
    });
  }

  async toggleComplete(id: number) {
    return this.request(`/api/v1/tasks/${id}/complete`, {
      method: 'PATCH'
    });
  }
}

export const api = new ApiClient();
```

---

## Related Specifications

- **Overview:** `@specs/overview.md`
- **Architecture:** `@specs/architecture.md`
- **Features:** `@specs/features/`
- **Database:** `@specs/database/schema.md`
- **UI:** `@specs/ui/`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
