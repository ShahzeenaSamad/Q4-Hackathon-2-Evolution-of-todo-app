# Skill: FastAPI Backend Implementation

## Metadata

**Skill Name:** `fastapi-backend`

**Description:** Implement FastAPI applications with SQLModel, JWT auth, RESTful APIs, and PostgreSQL integration.

**Version:** 1.0

**Author:** Claude Code

**Created:** January 17, 2026

---

## Purpose

This skill implements production-ready FastAPI backend applications following best practices for:
- RESTful API design
- JWT-based authentication
- SQLModel ORM with PostgreSQL
- Secure coding practices
- Error handling and logging
- API documentation

---

## When to Use

Use this skill when:
- Implementing FastAPI backend endpoints
- Creating RESTful APIs
- Setting up authentication with JWT
- Integrating with PostgreSQL database
- Creating database models with SQLModel
- Building middleware and dependencies
- Writing API tests

**Prerequisites:**
- Python 3.13+ installed
- Basic FastAPI concepts understood
- Database schema approved and specified

---

## Core Principles

1. **Spec-Driven Implementation:** Follow approved specifications exactly
2. **Security First:** JWT verification on all protected routes
3. **Data Isolation:** Filter all queries by user_id
4. **API-First:** RESTful conventions, proper status codes
5. **Type Safety:** Use Pydantic models for validation
6. **Error Handling:** Comprehensive exception handling with user-friendly messages

---

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── models.py               # SQLModel database models
├── db.py                   # Database connection & session
├── auth.py                 # JWT utilities & middleware
├── routes/
│   ├── auth.py             # Authentication endpoints
│   └── tasks.py            # Feature-specific endpoints
├── schemas/
│   ├── task.py             # Pydantic models for validation
│   └── user.py
├── utils/
│   ├── errors.py           # Custom error handlers
│   └── validators.py       # Input validation utilities
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md               # Documentation
```

---

## Implementation Patterns

### 1. Database Models (SQLModel)

**Pattern:**
```python
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class TaskBase(SQLModel):
    """Base model with common fields"""
    title: str = Field(max_length=200)
    description: Optional[str] = None

class Task(TaskBase, table=True):
    """Table model"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Rules:**
- ✅ Use SQLModel base classes
- ✅ Add table=True for database tables
- ✅ Foreign keys with Field(foreign_key="table.column")
- ✅ Indexes on frequently queried fields
- ✅ Default values with default_factory
- ✅ Type hints for all fields

---

### 2. Database Connection

**Pattern:**
```python
from sqlmodel import create_engine, Session
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,                    # Log SQL in dev
    pool_pre_ping=True,            # Verify connections
    pool_size=10,                  # Connection pool
    max_overflow=20               # Extra connections
)

def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
```

**Rules:**
- ✅ Use environment variable for DATABASE_URL
- ✅ Enable echo in development, disable in production
- ✅ Configure connection pooling
- ✅ Use dependency injection for sessions

---

### 3. JWT Authentication

**Pattern:**
```python
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from os import getenv

JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

def verify_jwt(request: Request):
    """Verify JWT token and extract user_id"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing token")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(401, "Invalid token")

        request.state.user_id = user_id
        return user_id

    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
```

**Usage:**
```python
@app.get("/api/v1/tasks", dependencies=[Depends(verify_jwt)])
async def get_tasks(request: Request):
    user_id = request.state.user_id
    # Fetch tasks for this user only
```

**Rules:**
- ✅ JWT secret from environment variable
- ✅ HS256 algorithm
- ✅ Extract user_id from "sub" claim
- ✅ Attach user_id to request.state
- ✅ Raise 401 for invalid/expired tokens
- ✅ Return 401 if Authorization header missing

---

### 4. API Endpoints

**GET Endpoint (List):**
```python
@app.get("/api/v1/tasks")
async def get_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query("all", regex="^(all|pending|completed)$"),
    session: Session = Depends(get_session),
    user_id: str = Depends(verify_jwt)
):
    """Get all tasks for authenticated user"""
    # Build query with user filter
    query = select(Task).where(Task.user_id == user_id)

    # Apply filters
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Get total count
    total = len(session.exec(query).all())

    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    tasks = session.exec(query).all()

    return {
        "success": True,
        "data": {
            "tasks": tasks,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": (total + limit - 1) // limit
            }
        }
    }
```

**POST Endpoint (Create):**
```python
@app.post("/api/v1/tasks", status_code=201)
async def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(verify_jwt)
):
    """Create a new task"""
    # Validate input
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(400, {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Title is required"
            }
        })

    # Create with user_id
    task = Task(
        user_id=user_id,
        title=task_data.title.strip(),
        description=task_data.description
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task
    }
```

**Rules:**
- ✅ All endpoints use dependencies=[Depends(verify_jwt)]
- ✅ Return consistent response format (success, data/error)
- ✅ Use Query() for query parameters
- ✅ Validate inputs before database operations
- ✅ Filter all queries by user_id
- ✅ Use appropriate HTTP status codes
- ✅ Include docstrings for OpenAPI docs

---

### 5. Pydantic Schemas

**Request Models:**
```python
from pydantic import BaseModel, Field, EmailStr

class TaskCreate(BaseModel):
    """Schema for creating a task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
```

**Response Models:**
```python
class TaskRead(BaseModel):
    """Schema for task response"""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

**Rules:**
- ✅ Use Pydantic BaseModel for request/response
- ✅ Add validation with Field(...) constraints
- ✅ Optional fields for partial updates
- ✅ Email validation with EmailStr type
- ✅ Custom validators for complex logic

---

### 6. Error Handling

**Custom Exceptions:**
```python
from fastapi import HTTPException

class ValidationError(HTTPException):
    """Validation error response"""
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=400,
            detail={
                "success": False,
                "error": {
                    "code": code,
                    "message": message
                }
            }
        )

class NotFoundError(HTTPException):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": message
                }
            }
        )
```

**Usage:**
```python
if not task_data.title:
    raise ValidationError("Title is required")

if not task:
    raise NotFoundError("Task not found")
```

---

### 7. Security Best Practices

#### Data Isolation
```python
# WRONG - Returns all tasks (INSECURE!)
tasks = session.query(Task).all()

# CORRECT - Returns only user's tasks (SECURE!)
tasks = session.query(Task).filter(Task.user_id == user_id).all()
```

#### Input Validation
```python
# Sanitize user input
title = task_data.title.strip()
description = task_data.description.strip() if task_data.description else None

# Strip HTML tags (basic sanitization)
import re
description = re.sub(r'<[^>]+>', '', description)
```

#### SQL Injection Prevention
```python
# SQLModel automatically handles this
# NEVER use string concatenation for queries
task = Task(user_id=user_id, title=title)  # ✅ SAFE
```

---

### 8. CORS Configuration

**Pattern:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Dev
        "https://your-app.vercel.app"  # Prod
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 9. API Documentation

**Automatic with FastAPI:**
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

**Add Documentation:**
```python
@app.get("/api/v1/tasks", tags=["Tasks"])
async def get_tasks(
    page: int = Query(1, description="Page number"),
    limit: int = Query(20, description="Items per page"),
    status: str = Query("all", description="Filter by status")
):
    """
    Get all tasks for the authenticated user.

    Returns paginated list of tasks filtered by status.

    - **page**: Page number (starts at 1)
    - **limit**: Items per page (max 100)
    - **status**: Filter by "all", "pending", or "completed"
    """
    # Implementation...
```

---

### 10. Environment Configuration

**.env.example:**
```env
# Database
DATABASE_URL=postgresql://user:pass@host/database

# JWT
JWT_SECRET=your-secret-key-min-32-characters

# Frontend (CORS)
FRONTEND_URL=http://localhost:3000
```

**Load in Python:**
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Testing Strategy

### Unit Tests
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session

def test_create_task():
    """Test task creation"""
    client = TestClient(app)

    # Create user and get token
    token = signup_and_get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "Test"},
        headers=headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert data["data"]["title"] == "Test Task"
```

---

## Quality Checklist

Before completing implementation:

- [ ] All protected routes use verify_jwt dependency
- [ ] All database queries filter by user_id
- [ ] Input validation with Pydantic models
- [ ] Error responses follow consistent format
- [ ] CORS configured for frontend
- [ ] Database indexes created
- [ ] API documentation complete
- [ ] Environment variables documented
- [ ] Tests written for all endpoints
- [ ] Security review passed

---

## Common Patterns

### Pattern 1: Paginated List
```python
@app.get("/api/v1/tasks")
async def list_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
    user_id: str = Depends(verify_jwt)
):
    query = select(Task).where(Task.user_id == user_id)
    total = len(session.exec(query).all())

    query = query.offset((page - 1) * limit).limit(limit)
    items = session.exec(query).all()

    return {
        "success": True,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit
        }
    }
```

### Pattern 2: Get by ID with Ownership Check
```python
@app.get("/api/v1/tasks/{task_id}")
async def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(verify_jwt)
):
    # User can only see their own tasks
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # CRITICAL: Data isolation
        )
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    return {"success": True, "data": task}
```

### Pattern 3: Update with Partial Fields
```python
@app.put("/api/v1/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(verify_jwt)
):
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    # Update only provided fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return {"success": True, "data": task}
```

---

## Dependencies

### Required Python Packages:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic==2.5.3
email-validator==2.1.0
```

### Install:
```bash
pip install -r requirements.txt
```

---

## Related Skills

- `spec-writing` - Create specifications before implementing
- `system-architecture` - Design architecture before coding
- `qa-testing-validator` - Test implementation after completion

---

## Usage Instructions

When invoked, this skill will:

1. **Read Specification:** Review approved specs and architecture
2. **Setup Project:** Create necessary files and structure
3. **Implement Models:** Create SQLModel database models
4. **Implement Auth:** Setup JWT authentication
5. **Create Endpoints:** Build RESTful API endpoints
6. **Add Validation:** Implement input validation with Pydantic
7. **Configure Security:** Add CORS, error handling
8. **Write Tests:** Create unit and integration tests
9. **Document:** Add API documentation
10. **Validate:** Test all endpoints work correctly

---

## File Locations

Implementation creates:
- Backend code: `backend/` directory
- Database models: `backend/models.py`
- Routes: `backend/routes/` directory
- Tests: `backend/tests/` directory
- Docs: `backend/README.md`

---

## Version History

- **v1.0** (2026-01-17): Initial skill definition

---

**Skill Status:** ✅ Active
**Phase:** Phase II - Full-Stack Web Application
