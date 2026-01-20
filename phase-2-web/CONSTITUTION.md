# CONSTITUTION.md
# Hackathon II: Phase 2 - Full-Stack Web Application

## Project Identity

**Project Name:** Evolution of Todo – Phase 2 Full-Stack Web Application

**Current Phase:** Phase II: Full-Stack Web Application

**Vision:** Transform the Phase I console app into a modern, multi-user web application with persistent storage, following spec-driven development principles.

**Long-term Goal:** Create a reusable blueprint for AI-driven software development demonstrating the Nine Pillars of AI-Driven Development.

---

## Core Principles

### 1. Spec-Driven Development (MANDATORY)

- **Mandatory:** Every feature, component, and system must have a written specification before implementation
- **Iterative Refinement:** Specifications must be refined until they produce correct outputs when implemented by Claude Code
- **Reference Standard:** All code must reference specifications using `@specs/` path conventions
- **No Manual Coding:** Implementation must be generated exclusively through Claude Code based on approved specs
- **Spec-First:** Specifications must be created before implementation begins

---

### 2. Security-First Architecture (MANDATORY)

- **Zero Trust:** Implement authentication and authorization from Phase II onwards
- **JWT Standard:** Use JWT tokens for stateless authentication
- **User Data Isolation:** Enforce user data isolation at all layers
  - Every database query MUST filter by authenticated user_id
  - Frontend-provided user_id MUST never be trusted without JWT verification
- **Secret Management:** Never hardcode secrets; use environment variables
- **Data Protection:** Encryption of sensitive data at rest and in transit

---

### 3. Separation of Concerns

- **Clear Boundaries:** Frontend and backend must have well-defined API contracts
- **Independent Development:** Frontend and backend should be developable independently
- **Contract Testing:** API contracts must be tested for compatibility
- **Version Alignment:** Frontend and backend versions must be synchronized

---

### 4. Stateful Design with State Isolation

- **Stateless Services:** All services must be stateless with external state management
- **Database-Backed Memory:** Conversation and application state stored in database
- **State Isolation:** User state strictly isolated, no cross-user data leakage

---

### 5. API-First Design

- **Contract First:** API specifications must be written before implementation
- **Versioning Strategy:** Use semantic versioning for APIs (`/api/v1/`, `/api/v2/`)
- **Documentation:** Complete API documentation with examples
- **Spec References:** All API endpoints must reference `@specs/api/rest-endpoints.md`

---

## Key Standards

### 1. API Endpoint Standards (MANDATORY)

**Every REST API endpoint MUST:**

**Require Authentication:**
- All endpoints (except signup/login) MUST require: `Authorization: Bearer <JWT>`
- JWT must be validated using shared `BETTER_AUTH_SECRET` environment variable

**Validate JWT:**
- Extract user_id from JWT "sub" claim
- Verify token signature with HS256 algorithm
- Reject expired or invalid tokens with 401 Unauthorized

**Filter by User:**
- Every query MUST include: `WHERE user_id = ?` filter
- Backend MUST NOT trust frontend-provided user_id
- Enforce task ownership on Read/Create/Update/Delete operations

**Return JSON:**
- All responses must be JSON format
- Follow defined schema exactly
- Include success/error flags

**Example:**
```python
@app.get("/api/v1/tasks", dependencies=[Depends(verify_jwt)])
async def get_tasks(
    user_id: str = Depends(verify_jwt),  # From JWT
    session: Session = Depends(get_session)
):
    # MUST filter by user_id
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return {"success": True, "data": {"tasks": tasks}}
```

---

### 2. Database Standards (MANDATORY)

**Access Control:**
- Use SQLModel ORM only (no raw SQL unless absolutely necessary)
- All queries MUST include user_id filter
- Foreign keys enforce relationships

**Schema Compliance:**
- Database schema MUST match `@specs/database/schema.md` exactly
- Indexes must be created on user_id and completed fields

**Example:**
```python
# CORRECT - Enforces data isolation
def get_user_tasks(user_id: str):
    return session.query(Task).filter(Task.user_id == user_id).all()

# WRONG - Returns all tasks (SECURITY RISK!)
def get_all_tasks():
    return session.query(Task).all()
```

---

### 3. Spec-Kit Structure (MANDATORY)

**Required Folder Structure:**
```
specs/
├── overview.md                # Project overview
├── architecture.md            # System architecture
├── features/                  # Feature specifications
│   ├── task-crud.md          # Task CRUD operations
│   ├── authentication.md     # User authentication
│   └── ...                   # Future features
├── api/                      # API specifications
│   ├── rest-endpoints.md     # REST API contract
│   └── ...                   # Additional API specs
├── database/                 # Database specifications
│   ├── schema.md             # Database schema
│   └── ...                   # Migration docs
└── ui/                       # UI specifications
    ├── components.md         # UI components
    ├── pages.md              # Page layouts
    └── ...                   # Additional UI specs
```

**Must Follow:**
- All features need specifications before implementation
- All implementations must reference specs using `@specs/` paths
- No code without specs

---

### 4. CLAUDE.md File Standards

**Root CLAUDE.md:**
- Guides overall navigation and spec usage
- References all major specs
- Defines development workflow

**Backend CLAUDE.md:**
- Backend-specific patterns and conventions
- API development guidelines
- Database interaction patterns

**Frontend CLAUDE.md:**
- Frontend-specific patterns (Next.js 16+)
- Component design patterns
- API integration patterns

---

### 5. Backend Route Standards (MANDATORY)

**All backend routes MUST:**

- Be under `/api/` prefix
- Use FastAPI with proper typing
- Include Pydantic models for validation
- Handle errors with appropriate HTTP status codes:
  - 200: Success
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized (missing/invalid token)
  - 403: Forbidden (access denied)
  - 404: Not Found
  - 500: Internal Server Error

---

### 6. Security Rules (MANDATORY)

**Authentication:**
- Signup/Login: Public endpoints (no JWT required)
- All other endpoints: Require JWT token
- Token must be extracted from `Authorization: Bearer <token>` header

**Authorization:**
- Backend MUST verify JWT signature
- Backend MUST extract user_id from JWT
- Backend MUST reject expired/invalid tokens

**Data Isolation:**
- Every operation MUST check user_id matches authenticated user
- No cross-user data access allowed

**Example:**
```python
# Enforce data isolation
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id  # Must match JWT user_id
).first()

if not task or task.user_id != user_id:
    raise HTTPException(403, "Access Denied")
```

---

### 7. Response Format Standards (MANDATORY)

**Success Response:**
```json
{
  "success": true,
  "data": {...}
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

---

## Phase II Specific Requirements

### Technology Stack (LOCKED)

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | Next.js 16+ (App Router) | ✅ Locked |
| Backend | FastAPI | ✅ Locked |
| ORM | SQLModel | ✅ Locked |
| Database | Neon Serverless PostgreSQL | ✅ Locked |
| Authentication | Better Auth + JWT | ✅ Locked |
| Spec-Driven | Claude Code + Spec-Kit Plus | ✅ Locked |

### Scope

**Included:**
- ✅ Task CRUD operations (Create, Read, Update, Delete, Toggle Complete)
- ✅ User authentication (signup, login, logout)
- ✅ JWT authentication with 7-day expiry
- ✅ Responsive frontend UI
- ✅ RESTful API with proper error handling
- ✅ PostgreSQL database with user data isolation
- ✅ Swagger/OpenAPI documentation

**Deferred to Phase III:**
- AI chatbot features
- Recurring tasks
- Reminders
- Real-time sync
- Advanced features

---

## Development Standards

### Spec-First Workflow

**Phase 1: SPECIFY**
- Write comprehensive specification documents
- Follow Spec-Kit folder structure
- Get approval before implementation

**Phase 2: PLAN**
- Create architecture design
- Design database schema
- Plan API contracts

**Phase 3: CLARIFY**
- Ask user for approvals
- Freeze specifications
- Document decisions

**Phase 4: TASK**
- Create task breakdown
- Assign to agents
- Define acceptance criteria

**Phase 5: IMPLEMENTATION**
- Agents implement strictly according to specs
- No manual coding allowed
- Test against specs

---

## Quality Standards

### Code Quality

- **Consistency:** Follow established patterns and conventions
- **Readability:** Clear, well-structured code
- **Documentation:** Complete docstrings for classes and functions
- **Type Safety:** TypeScript for frontend, type hints for backend
- **Error Handling:** Comprehensive error handling with user-friendly messages

### Testing Requirements

- **Unit Tests:** Core functionality must have unit tests
- **Integration Tests:** API endpoints must have integration tests
- **E2E Tests:** Critical user flows must be end-to-end tested
- **Performance Tests:** API responses < 300ms (p95)

---

## Security Standards

### Authentication

- **JWT-Based:** All authentication uses JWT tokens
- **Stateless:** No server-side sessions
- **Token Expiry:** 7 days (configurable via BETTER_AUTH_SECRET)
- **Token Storage:** HTTP-only cookies (XSS prevention)

### Authorization

- **User Isolation:** Users can only access their own data
- **Route Protection:** All protected routes require valid JWT
- **Ownership Verification:** Check user_id on all operations

### Data Protection

- **SQL Injection Prevention:** Use parameterized queries (SQLModel)
- **XSS Prevention:** Framework auto-escaping
- **CSRF Prevention:** SameSite cookies + JWT verification
- **Input Validation:** Comprehensive validation on all inputs

---

## API Endpoint Rules

### All Endpoints Follow:

**Authentication:**
```
POST /api/v1/auth/signup     → Public
POST /api/v1/auth/login      → Public
GET  /api/v1/auth/me         → Protected (requires JWT)
```

**Tasks:**
```
GET    /api/v1/tasks         → Protected
POST   /api/v1/tasks         → Protected
GET    /api/v1/tasks/{id}     → Protected
PUT    /api/v1/tasks/{id}     → Protected
DELETE /api/v1/tasks/{id}     → Protected
PATCH  /api/v1/tasks/{id}/complete → Protected
```

**Other:**
```
GET /api/v1/health          → Public
```

---

## Backend/Frontend Integration

### Better Auth + FastAPI Integration

**JWT Configuration:**
```yaml
# Frontend (Better Auth)
JWT:
  enabled: true
  expiresIn: "7d"
```

**Backend JWT Verification:**
```python
# Backend (FastAPI)
import jose

def verify_jwt(token: str) -> dict:
    try:
        payload = jose.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jose.JWTError:
        raise HTTPException(401, "Invalid token")
```

**Shared Secret:**
```bash
# Both frontend and backend MUST use same secret
BETTER_AUTH_SECRET=your-secret-key-here-min-32-characters
```

---

## Compliance & Validation

### Pre-Implementation Checklist

- [ ] All specifications reviewed and approved
- [ ] Database schema matches specs exactly
- [ ] API endpoints match `@specs/api/rest-endpoints.md`
- [ ] Environment variables configured
- [ ] JWT secret shared between frontend and backend
- [ ] All routes protected with JWT verification
- [ ] Data isolation enforced on all queries
- [ ] Error responses follow standard format

### Post-Implementation Validation

- [ ] All endpoints tested
- [ ] Data isolation verified (user can't see other users' data)
- [ ] JWT authentication tested
- [ ] API responses match schema
- [ ] Error handling tested
- [ ] Performance budgets met (< 300ms p95 for APIs)

---

## Phase II Deliverables

### Required Deliverables

1. **Specifications:** 8 spec documents (created ✅)
   - overview.md
   - architecture.md
   - features/task-crud.md
   - features/authentication.md
   - api/rest-endpoints.md
   - database/schema.md
   - ui/components.md
   - ui/pages.md

2. **Backend:** FastAPI application (implemented ✅)
   - All REST API endpoints
   - JWT authentication middleware
   - PostgreSQL integration
   - API documentation

3. **Frontend:** Next.js 16+ application (pending)
   - App Router structure
   - Better Auth integration
   - API client integration
   - Responsive UI components

4. **Tests:** All tests passing (pending)

---

## Version History

- **v1.0:** Initial constitution for Hackathon II
  - Ratification: January 16, 2026
  - Effective: Phase I (Console App)
  - Governance: All development activities

- **v2.0:** Phase II Update
  - Date: January 17, 2026
  - Changes:
    - Added Phase II specific requirements
    - Locked technology stack
    - Enforced API endpoint standards
    - Added security rules (JWT, data isolation)
    - Defined backend/frontend integration
    - Locked development workflow (spec → plan → clarify → task → implement)

---

## Signatories

**Project Architect:** [Your Name]
**Date:** January 16, 2026

**Phase II Update:**
- **Spec-Driven Development:** All code must be implemented from specs
- **Security-First:** JWT authentication with user data isolation
- **API-First:** All endpoints must follow defined specs
- **No Manual Coding:** No code generation without specs

---

**Note:** This is the governing document for Phase II development. All development activities must comply with these principles. Changes require re-approval and version update.

---

**Status:** ✅ Active
**Phase:** Phase II - Full-Stack Web Application
