# Todo App - Project Overview

## Project Identity

**Project Name:** Evolution of Todo – From Console to Cloud-Native AI

**Current Phase:** Phase II: Full-Stack Web Application

**Vision:** Transform the Phase I console app into a modern, multi-user web application with persistent storage and authentication.

---

## Phase Overview

### Phase I: Console App ✅ (Completed)
- **Status:** Complete (70/70 tasks, 100% test coverage)
- **Tech Stack:** Python 3.13+, In-memory storage
- **Features:** Add, View, Update, Delete, Complete tasks
- **Location:** `/phase-1-console/`

### Phase II: Full-Stack Web Application 🚧 (In Progress)
- **Status:** Specification Phase
- **Objective:** Multi-user web app with persistent storage
- **Key Features:** Task CRUD, User Authentication, RESTful API, Responsive UI
- **Location:** `/phase-2-web/`

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 16+ (App Router) | React-based UI framework |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **Backend** | Python FastAPI | High-performance async API |
| **ORM** | SQLModel | SQLAlchemy + Pydantic integration |
| **Database** | Neon Serverless PostgreSQL | Cloud-native PostgreSQL |
| **Authentication** | Better Auth + JWT | Stateless user authentication |
| **Spec-Driven** | Claude Code + Spec-Kit Plus | AI-powered development |
| **Deployment** | Vercel (Frontend) | Serverless hosting |

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Next.js Frontend                            │
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │  Better Auth    │    │  React Components│               │
│  │  (JWT Client)   │    │  - TaskList      │               │
│  └────────┬────────┘    │  - TaskForm      │               │
│           │              │  - AuthPages     │               │
│           │              └──────────────────┘               │
└───────────┼─────────────────────────────────────────────────┘
            │
            │ HTTP + JWT Token
            ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend                             │
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │ JWT Middleware  │    │  API Routes      │               │
│  │ - Verify Token  │───▶│  - GET /tasks    │               │
│  │ - Extract User  │    │  - POST /tasks   │               │
│  └─────────────────┘    │  - PUT /tasks    │               │
│                         │  - DELETE /tasks │               │
│                         └────────┬─────────┘               │
└──────────────────────────────────┼──────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Neon Serverless PostgreSQL                      │
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │  users table    │    │   tasks table    │               │
│  │  (Better Auth)  │    │  - user_id (FK)  │               │
│  └─────────────────┘    │  - title         │               │
│                         │  - description   │               │
│                         │  - completed     │               │
│                         │  - created_at    │               │
│                         └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Features

### 1. User Authentication
- **Signup:** User registration with email/password
- **Login:** JWT token issuance upon authentication
- **Session Management:** Stateless JWT-based sessions
- **Data Isolation:** Each user sees only their own tasks

### 2. Task Management (CRUD)
- **Create Task:** Add new tasks with title and optional description
- **View Tasks:** List all user's tasks with filtering and sorting
- **Update Task:** Modify task title and description
- **Delete Task:** Remove tasks from the list
- **Complete Task:** Toggle task completion status

### 3. API Design
- **RESTful:** Follow REST conventions
- **Stateless:** No session storage on backend
- **JWT-Secured:** All endpoints require valid JWT token
- **User-Scoped:** All operations filtered by user ID

---

## Security Architecture

### JWT Token Flow

1. **User Login (Frontend):**
   ```
   User → Better Auth → Verify Credentials
                        ↓
                     Issue JWT Token
                        ↓
                   Store in Cookie/LocalStorage
   ```

2. **API Request (Frontend → Backend):**
   ```
   Frontend → Add JWT to Authorization Header
            ↓
   Backend → JWT Middleware → Verify Token Signature
                              ↓
                         Extract user_id
                              ↓
                       Pass to Route Handler
   ```

3. **Data Access (Backend):**
   ```
   Route Handler → Filter all queries by user_id
                 ↓
           Return only user's data
   ```

---

## Data Model

### Users Table (Managed by Better Auth)
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Tasks Table
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
```

---

## API Endpoints Overview

All endpoints require `Authorization: Bearer <jwt_token>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List all user's tasks |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/{id}` | Get specific task details |
| PUT | `/api/tasks/{id}` | Update a task |
| DELETE | `/api/tasks/{id}` | Delete a task |
| PATCH | `/api/tasks/{id}/complete` | Toggle task completion |

---

## Frontend Pages

| Page | Route | Purpose |
|------|-------|---------|
| Login | `/login` | User authentication |
| Signup | `/signup` | New user registration |
| Dashboard | `/dashboard` | Main task management interface |
| Task Detail | `/tasks/{id}` | View/edit individual task |

---

## Development Workflow

### 1. Specification Phase (Current)
- ✅ Create all feature specifications
- ✅ Define API contracts
- ✅ Design database schema
- ✅ Plan UI components

### 2. Backend Implementation
- Setup FastAPI project structure
- Implement database models
- Create JWT middleware
- Build REST API endpoints
- Write tests

### 3. Frontend Implementation
- Setup Next.js project
- Configure Better Auth
- Build UI components
- Create API client
- Implement pages

### 4. Integration & Testing
- Connect frontend to backend
- Test authentication flow
- Verify data isolation
- Performance testing

### 5. Deployment
- Deploy frontend to Vercel
- Deploy backend to cloud
- Configure environment variables
- End-to-end validation

---

## Success Criteria

### Functional Requirements
- ✅ Users can signup and login
- ✅ Users can create, read, update, and delete tasks
- ✅ Each user only sees their own tasks
- ✅ JWT tokens secure all API requests
- ✅ Responsive UI works on mobile and desktop

### Non-Functional Requirements
- ⚡ API response time < 300ms (p95)
- 🔒 All endpoints protected with JWT
- 📊 Database queries properly indexed
- 🧪 All endpoints have integration tests
- 📱 Frontend is mobile-responsive

---

## Next Steps

**Current Phase:** Specification Creation

**Immediate Actions:**
1. ✅ Review this overview
2. ⏭️ Read architecture specification
3. ⏭️ Review feature specifications
4. ⏭️ Approve specifications before implementation

**After Approval:**
- Begin backend implementation
- Follow spec-driven development workflow
- Use Claude Code for all code generation
- Maintain specification accuracy

---

## Related Specifications

- **Architecture:** `@specs/architecture.md`
- **Features:** `@specs/features/`
- **API:** `@specs/api/rest-endpoints.md`
- **Database:** `@specs/database/schema.md`
- **UI:** `@specs/ui/`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
