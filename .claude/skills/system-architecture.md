# Skill: System Architecture

## Metadata

**Skill Name:** `system-architecture`

**Description:** Design scalable, secure architecture including frontend-backend separation, JWT flows, and database relationships.

**Version:** 1.0

**Author:** Claude Code

**Created:** January 17, 2026

---

## Purpose

This skill designs comprehensive, production-ready system architectures for web applications, emphasizing:
- Scalability and performance
- Security best practices
- Frontend-backend separation
- JWT authentication flows
- Database design and relationships
- Cloud-native principles

---

## When to Use

Use this skill when:
- Designing overall system architecture
- Planning frontend-backend integration
- Designing authentication and authorization flows
- Creating database schemas and relationships
- Planning API contracts and boundaries
- Designing microservices or distributed systems
- Planning deployment architecture

---

## Core Principles

1. **Separation of Concerns:** Clear boundaries between frontend, backend, and database
2. **Security by Design:** Zero Trust, JWT-based stateless authentication
3. **Stateless Design:** No server-side sessions, horizontal scaling
4. **API-First:** Clear API contracts before implementation
5. **Data Isolation:** User data enforced at database level
6. **Cloud-Native:** Container-ready, Kubernetes-friendly

---

## Architecture Components

### 1. Frontend Architecture

**Responsibilities:**
- User interface rendering
- Client-side routing
- Authentication UI (JWT storage)
- API communication
- State management

**Best Practices:**
- Use server components by default
- Client components only for interactivity
- Store JWT in HTTP-only cookies
- Validate responses from backend

**Technology Stack Options:**
- Next.js 14+ (App Router)
- React 18+
- TypeScript
- Tailwind CSS

---

### 2. Backend Architecture

**Responsibilities:**
- Business logic implementation
- JWT verification and user identification
- Data validation and sanitization
- Database operations
- API endpoint management

**Best Practices:**
- Stateless design (no session storage)
- JWT middleware on all protected routes
- User data filtering at database level
- Comprehensive error handling
- Input validation with Pydantic

**Technology Stack Options:**
- Python FastAPI
- Node.js Express
- Go Gin/Echo
- Java Spring Boot

---

### 3. Authentication Architecture

#### JWT Token Flow

```
┌─────────────┐         ┌──────────────┐
│   Frontend  │         │   Backend     │
│             │         │              │
│  1. Login   │────────▶│  2. Verify   │
│             │         │     Token     │
│             │         │              │
│  3. Store   │◀────────│  4. Extract   │
│    JWT      │  Token  │    user_id    │
└─────────────┘         └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Database   │
                     │              │
                     │  Filter by   │
                     │  user_id     │
                     └──────────────┘
```

**JWT Token Structure:**
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "name": "User Name",
  "iat": 1737106200,
  "exp": 1737711000
}
```

**Security Rules:**
- All protected routes require valid JWT
- Token signed with HS256 algorithm
- Secret key shared between frontend and backend
- Token expiration: 7 days (configurable)
- HTTP-only cookies prevent XSS

---

### 4. Database Architecture

#### Data Isolation Pattern

**CRITICAL:** Every database query MUST filter by user_id

```python
# WRONG - Returns ALL tasks (INSECURE!)
SELECT * FROM tasks

# CORRECT - Returns only user's tasks (SECURE)
SELECT * FROM tasks WHERE user_id = ?
```

#### Table Relationships

```
┌─────────────┐
│    users    │
├─────────────┤
│ id (PK)     │◀──────────────┐
│ email       │               │
│ name        │               │
│ created_at  │               │
└─────────────┘               │
                              │
                    ┌────────▼────────┐
                    │     tasks       │
                    ├─────────────────┤
                    │ id (PK)         │
                    │ user_id (FK)   │
                    │ title           │
                    │ description    │
                    │ completed       │
                    │ created_at      │
                    │ updated_at      │
                    └─────────────────┘
```

**Constraints:**
- Foreign key: `tasks.user_id` references `users.id`
- Cascade delete: When user deleted, delete all tasks
- Indexes: `tasks.user_id`, `tasks.completed`, `tasks.created_at`

---

### 5. API Architecture

#### RESTful Conventions

**Base URL:** `/api/v1`

**Authentication Header:**
```
Authorization: Bearer <jwt_token>
```

**Response Format:**
```json
{
  "success": true|false,
  "data": {...},
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (access denied)
- 404: Not Found
- 500: Internal Server Error

---

### 6. Security Architecture

#### Threat Model & Mitigations

| Threat | Mitigation |
|--------|------------|
| **SQL Injection** | Parameterized queries (ORM) |
| **XSS** | Framework auto-escaping, input sanitization |
| **CSRF** | SameSite cookies, JWT verification |
| **Data Leakage** | User filtering at DB level, JWT validation |
| **Token Theft** | HTTPS, HTTP-only cookies, short expiration |
| **Unauthorized Access** | JWT required on all protected routes |

#### Data Isolation Enforcement

**Frontend:**
- Cannot make requests without valid JWT
- Token automatically attached to all API calls

**Backend:**
- JWT middleware verifies token on every request
- user_id extracted and attached to request.state
- All database queries filtered by user_id

**Database:**
- Foreign key constraints enforce relationships
- Indexes optimize user-specific queries

---

### 7. Scalability Architecture

#### Horizontal Scaling

**Frontend (Vercel):**
- Edge functions auto-scale
- Serverless compute
- Global CDN distribution

**Backend (Railway/Render):**
- Load balancer distributes requests
- Multiple server instances
- Stateless design allows any instance to handle any request

**Database (Neon PostgreSQL):**
- Serverless auto-scaling
- Connection pooling
- Read replicas (future)

#### Performance Optimization

**Caching Strategy:**
- Response caching for static data
- Query result caching (Redis/Native)
- CDN for static assets

**Database Optimization:**
- Indexed queries (user_id, completed, created_at)
- Connection pooling
- Query optimization with EXPLAIN

---

### 8. Deployment Architecture

#### Development Environment

```
Local Machine:
├── Frontend (localhost:3000)
├── Backend (localhost:8000)
└── Database (SQLite or local PostgreSQL)
```

#### Production Environment

```
┌─────────────────────────────────────────────┐
│                  Cloud (Vercel/DigitalOcean)   │
│                                                │
│  ┌──────────────┐    ┌──────────────────┐    │
│  │   Frontend    │    │    Backend      │    │
│  │   (Vercel)    │    │  (Railway)      │    │
│  │               │    │                 │    │
│  └──────┬───────┘    └──────┬──────────┘    │
│         │                   │               │
│         │                   ▼               │
│         │          ┌───────────────┐       │
│         │          │  Neon DB       │       │
│         │          │  (Serverless)  │       │
│         │          └───────────────┘       │
└─────────────────────────────────────────────┘
```

---

## Architecture Decision Framework

When designing architecture, consider:

### 1. Performance
- Response time budgets (p95 < 300ms)
- Concurrent user capacity
- Database query optimization
- Caching strategy

### 2. Security
- Authentication and authorization
- Data encryption at rest and in transit
- Input validation and sanitization
- Rate limiting and DDoS protection

### 3. Scalability
- Horizontal scaling capability
- Database connection pooling
- Stateless design for load balancing
- Auto-scaling configuration

### 4. Reliability
- Error handling and recovery
- Health check endpoints
- Graceful degradation
- Backup and disaster recovery

### 5. Maintainability
- Code organization and modularity
- Documentation standards
- Testing strategy
- Deployment automation

---

## Architecture Artifacts

This skill produces:

1. **Architecture Diagrams** (ASCII or Mermaid)
2. **Component Specifications**
3. **Data Flow Diagrams**
4. **Security Model**
5. **Deployment Topology**
6. **Technology Stack Recommendations**
7. **Integration Points**

---

## Output Format

Architecture documentation in **Markdown** format with:

- ASCII diagrams for visual representation
- Tables for structured comparisons
- Code blocks only for configuration examples
- Clear section headers
- Bullet points for lists

---

## Quality Checklist

Before finalizing architecture, verify:

- [ ] All components clearly defined
- [ ] Security measures documented
- [ ] Data flows specified
- [ ] Scalability considered
- [ ] Technology stack justified
- [ ] Deployment plan included
- [ ] Database relationships defined
- [ ] API contracts specified
- [ ] Authentication flow documented
- [ ] Error handling strategy defined

---

## Related Skills

- `spec-writing` - Create specifications for architecture
- `fastapi-backend-implementer` - Implement architecture in backend
- `frontend-nextjs-builder` - Implement architecture in frontend
- `qa-testing-validator` - Validate implementation against architecture

---

## Usage Instructions

When invoked, this skill will:

1. **Understand Context:** Analyze requirements and constraints
2. **Design Components:** Define frontend, backend, database architecture
3. **Plan Integration:** Design JWT flows, API contracts, data isolation
4. **Consider Scalability:** Plan for growth and optimization
5. **Document:** Create comprehensive architecture document
6. **Review:** Verify against quality checklist
7. **Output:** Present architecture for user approval

---

## File Location

Architecture documents should be saved in:
- Project architecture: `specs/architecture.md`
- System architecture: `specs/overview.md` (includes architecture section)
- Specific component architecture: `specs/[component]/architecture.md`

---

## Example Architecture Output

```markdown
# System Architecture - Todo App Phase II

## High-Level Architecture

[ASCII diagram showing frontend → backend → database]

## Component Design

### Frontend (Next.js)
- App Router structure
- Client components for interactivity
- JWT token management

### Backend (FastAPI)
- JWT middleware
- API route handlers
- Database models

### Authentication Flow

1. User logs in → JWT issued
2. Frontend stores JWT in cookie
3. API calls include JWT in header
4. Backend verifies JWT
5. User data filtered by user_id

## Database Schema

[Table definitions and relationships]
```

---

## Version History

- **v1.0** (2026-01-17): Initial skill definition

---

**Skill Status:** ✅ Active
**Phase:** Phase II - Full-Stack Web Application
