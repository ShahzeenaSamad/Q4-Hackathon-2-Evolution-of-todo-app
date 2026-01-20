# System Architecture - Phase II

## Architecture Overview

This document describes the system architecture for Phase II: Full-Stack Web Application of the Todo App evolution.

---

## Architectural Principles

### 1. Separation of Concerns
- **Frontend:** UI and user interactions (Next.js)
- **Backend:** Business logic and data management (FastAPI)
- **Database:** Persistent storage (Neon PostgreSQL)
- **Auth:** Authentication service (Better Auth)

### 2. Stateless Design
- **No Server Sessions:** All session state in JWT tokens
- **Scalable:** Horizontal scaling without sticky sessions
- **Resilient:** Server restarts don't affect user sessions

### 3. API-First Development
- **Contract First:** API specs before implementation
- **Versioned:** All routes under `/api/v1/`
- **Documented:** OpenAPI/Swagger documentation

### 4. Security by Design
- **Zero Trust:** All endpoints require authentication
- **User Isolation:** Data filtered at database level
- **JWT Validation:** Token verification on every request

---

## Component Architecture

### Frontend Layer (Next.js)

```
frontend/
├── app/                      # App Router
│   ├── (auth)/              # Auth group
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/           # Main dashboard
│   └── layout.tsx           # Root layout
├── components/
│   ├── ui/                  # Reusable UI components
│   ├── forms/               # Form components
│   └── tasks/               # Task-specific components
└── lib/
    ├── api.ts               # API client
    ├── auth.ts              # Auth utilities
    └── db.ts                # Better Auth client
```

**Responsibilities:**
- User interface rendering
- Client-side routing
- Authentication UI (Better Auth)
- API communication
- State management (React hooks)

**Technology Stack:**
- Next.js 16+ (App Router)
- React 19+
- TypeScript
- Tailwind CSS
- Better Auth

---

### Backend Layer (FastAPI)

```
backend/
├── main.py                  # FastAPI app entry
├── models.py                # SQLModel database models
├── db.py                    # Database connection
├── auth/
│   ├── jwt.py               # JWT utilities
│   └── middleware.py        # JWT verification middleware
├── routes/
│   ├── tasks.py             # Task CRUD endpoints
│   └── auth.py              # Auth endpoints
├── schemas/
│   └── task.py              # Pydantic models
└── utils/
    ├── errors.py            # Error handlers
    └── validators.py        # Input validation
```

**Responsibilities:**
- RESTful API implementation
- JWT token verification
- Business logic enforcement
- Database operations
- Request validation
- Error handling

**Technology Stack:**
- Python 3.13+
- FastAPI
- SQLModel
- Pydantic
- python-jose (JWT)
- psycopg2 (PostgreSQL)

---

### Database Layer (Neon PostgreSQL)

**Schema:**
```sql
-- Users (managed by Better Auth)
users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP
)

-- Tasks (managed by our app)
tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
)

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

**Connection:**
- **ORM:** SQLModel (built on SQLAlchemy + Pydantic)
- **Connection Pooling:** Managed by SQLAlchemy
- **Migrations:** Alembic (if needed)

---

## Authentication Architecture

### Better Auth Integration

**Frontend (Next.js):**
```typescript
// Better Auth configuration
export const auth = betterAuth({
  database: db,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false
  },
  JWT: {
    enabled: true,
    expiresIn: "15m",    // Access token: 15-60 minutes
    refreshAge: "7d"     // Refresh token: 7 days
  }
})
```

**JWT Token Strategy (Clarified 2026-01-17):**
- **Access Token:** Short-lived (15-60 minutes) - limits exposure if compromised
- **Refresh Token:** Long-lived (7-30 days) - enables seamless session renewal
- **Refresh Endpoint:** `POST /api/v1/auth/refresh` - exchanges refresh token for new access token
- **Security:** Access tokens in memory, refresh tokens in httpOnly cookies

**Backend (FastAPI):**
```python
# JWT Verification Middleware
async def verify_jwt(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(401, "No token provided")

    payload = decode_jwt(token)
    user_id = payload.get("sub")
    request.state.user_id = user_id
```

### Token Flow

```
┌──────────┐         ┌──────────────┐         ┌──────────┐
│  User    │────────▶│  Next.js     │────────▶│ Better   │
│  Login   │         │  Frontend    │         │  Auth    │
└──────────┘         └──────────────┘         └─────┬────┘
                                                   │
                                                   │ Issue JWT
                                                   ▼
                                          ┌──────────────┐
                                          │ JWT Token    │
                                          │ - user_id    │
                                          │ - email      │
                                          │ - exp        │
                                          └──────────────┘
                                                   │
                                                   │ Store in Cookie
                                                   ▼
┌──────────┐         ┌──────────────┐         ┌──────────┐
│  API     │◀────────│  Next.js     │◀────────│  User    │
│  Request │         │  Frontend    │         | Request  │
└─────┬────┘         └──────────────┘         └──────────┘
      │
      │ Authorization: Bearer <token>
      ▼
┌──────────────┐
│  FastAPI     │
│  Middleware  │──▶ Verify JWT
│              │──▶ Extract user_id
└──────┬───────┘
       │
       │ user_id in request.state
       ▼
┌──────────────┐
│ Route Handler│──▶ Filter by user_id
└──────┬───────┘
       │
       │ User-scoped data
       ▼
┌──────────────┐
│  Response    │
└──────────────┘
```

---

## API Architecture

### RESTful Conventions

**Base URL:** `/api/v1`

**Authentication:**
- **Header:** `Authorization: Bearer <jwt_token>`
- **Required:** All endpoints
- **Error:** 401 Unauthorized if missing/invalid

**Response Format:**
```json
{
  "success": true/false,
  "data": {...},
  "error": "Error message if failed"
}
```

**Error Handling:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": {...}
  }
}
```

### Endpoints Categorization

**Public Routes:**
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token (requires valid refresh token)

**Protected Routes (Require JWT):**
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get task
- `PUT /api/v1/tasks/{id}` - Update task (with optimistic locking)
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PATCH /api/v1/tasks/{id}/complete` - Toggle completion
- `POST /api/v1/auth/logout` - Logout (invalidate refresh token)

---

## Data Flow Architecture

### Create Task Flow

```
User → Frontend Form
      ↓
Submit → API Client (POST /api/v1/tasks)
      ↓
HTTP Request + JWT Token
      ↓
FastAPI → JWT Middleware (Verify Token)
      ↓
Extract user_id → Route Handler
      ↓
Validate Input → Create Task Model
      ↓
Database → Insert with user_id
      ↓
Return Created Task
      ↓
Frontend → Update UI State
```

### List Tasks Flow

```
User → Dashboard Page
      ↓
API Client (GET /api/v1/tasks)
      ↓
HTTP Request + JWT Token
      ↓
FastAPI → JWT Middleware (Verify Token)
      ↓
Extract user_id → Route Handler
      ↓
Database → SELECT * FROM tasks WHERE user_id = ?
      ↓
Return User's Tasks Only
      ↓
Frontend → Render Task List
```

---

## Security Architecture

### Threat Model & Mitigations

| Threat | Mitigation |
|--------|------------|
| **Unauthorized Access** | JWT required on all endpoints |
| **Data Leakage** | **Backend-enforced user ID filtering on all queries** (authoritative enforcement) |
| **Cross-User Data Access** | Database queries scoped by user_id at backend level |
| **SQL Injection** | SQLModel parameterized queries |
| **XSS** | React automatic escaping |
| **CSRF** | SameSite cookies + JWT |
| **Token Theft** | HTTPS + Short-lived access tokens (15-60 min) |
| **Concurrent Edits** | Optimistic locking with HTTP 409 Conflict response |

### User Data Isolation (Clarified 2026-01-17)

**Enforcement Layer:** Backend is the authoritative enforcement layer
- Frontend filtering is for UX optimization only
- All database queries MUST include `WHERE user_id = ?` clause
- User attempting to access another user's resource receives HTTP 404 (prevents enumeration)

**Example Implementation:**
```python
# ❌ WRONG - Returns all tasks (INSECURE!)
def get_all_tasks():
    return session.query(Task).all()

# ✅ CORRECT - Returns only user's tasks (SECURE)
def get_user_tasks(user_id: str):
    return session.query(Task).filter(Task.user_id == user_id).all()
```

### Optimistic Locking (Clarified 2026-01-17)

**Purpose:** Prevent concurrent edit conflicts from multiple browser tabs

**Implementation:**
```python
# Update task with version check
task = session.get(Task, task_id)
if task.updated_at != request.updated_at:
    raise HTTPException(409, "Conflict: Task was modified by another client")

# Apply updates
task.title = request.title
task.updated_at = datetime.now()
session.add(task)
session.commit()
```

**Client Handling:**
- On HTTP 409: Fetch latest task state and prompt user to retry
- User can merge changes or overwrite with latest data

### Input Validation

**Frontend:**
- TypeScript type checking
- Form validation (react-hook-form)
- User-friendly error messages

**Backend:**
- Pydantic models for validation
- Length constraints (title: 200 chars, description: 1000 chars)
- Type coercion prevention
- Sanitization of user input

---

## Performance Architecture

### Optimization Strategies

**Database:**
- Indexed queries (user_id, completed, created_at)
- Connection pooling (SQLAlchemy)
- Query result caching (future)

**API:**
- Async operations (FastAPI)
- Efficient pagination (limit/offset)
- Response compression (gzip)

**Frontend:**
- Server Components (Next.js App Router)
- Static rendering where possible
- Code splitting by route
- Optimistic UI updates

---

## Deployment Architecture

### Development Environment

```
Local Machine:
├── Frontend (localhost:3000)
├── Backend (localhost:8000)
└── Database (Neon Cloud)
```

### Production Environment

```
┌─────────────────────────────────────┐
│         Vercel (Frontend)           │
│  ┌───────────────────────────────┐  │
│  │    Next.js App Router         │  │
│  │    - Static Assets (CDN)      │  │
│  │    - Edge Functions           │  │
│  │    - Auto HTTPS               │  │
│  └───────────────────────────────┘  │
└────────────┬────────────────────────┘
             │
             │ HTTPS + JWT
             ▼
┌─────────────────────────────────────┐
│    Railway/Render/Fly.io (Backend)  │
│  ┌───────────────────────────────┐  │
│  │    FastAPI Application        │  │
│  │    - Auto-scaling             │  │
│  │    - Load Balancer            │  │
│  └───────────────────────────────┘  │
└────────────┬────────────────────────┘
             │
             │ PostgreSQL Connection
             ▼
┌─────────────────────────────────────┐
│      Neon Serverless (Database)      │
│  ┌───────────────────────────────┐  │
│  │    PostgreSQL Database        │  │
│  │    - Auto-scaling storage     │  │
│  │    - Automatic backups        │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## Technology Justification

### Why Next.js 16+?
- ✅ Latest App Router with React Server Components
- ✅ Built-in TypeScript support
- ✅ Excellent developer experience
- ✅ Easy Vercel deployment
- ✅ Strong community support

### Why FastAPI?
- ✅ Native async support
- ✅ Automatic OpenAPI docs
- ✅ Pydantic validation built-in
- ✅ Fast performance (comparable to Node.js)
- ✅ Python ecosystem (SQLModel)

### Why SQLModel?
- ✅ SQLAlchemy + Pydantic combined
- ✅ Type-safe database models
- ✅ Easy to use
- ✅ Perfect for FastAPI

### Why Better Auth?
- ✅ Designed for Next.js
- ✅ JWT support out of the box
- ✅ TypeScript-first
- ✅ Easy integration with App Router

### Why Neon?
- ✅ Serverless PostgreSQL
- ✅ Free tier available
- ✅ Automatic scaling
- ✅ No connection pooling needed
- ✅ Branching for development

---

## Monitoring & Observability

### Logging Strategy

**Backend:**
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"User {user_id} created task {task_id}")
```

**Frontend:**
```typescript
console.log('[API] Creating task...', data);
// Sentry for error tracking (optional)
```

### Health Checks

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-17T10:30:00Z"
}
```

---

## Related Specifications

- **Overview:** `@specs/overview.md`
- **Features:** `@specs/features/`
- **API:** `@specs/api/rest-endpoints.md`
- **Database:** `@specs/database/schema.md`
- **UI:** `@specs/ui/`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
