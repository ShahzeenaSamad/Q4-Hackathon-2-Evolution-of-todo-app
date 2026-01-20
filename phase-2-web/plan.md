# Implementation Plan - Phase II: Full-Stack Web Application

**Created**: 2026-01-17
**Status**: Draft
**Based on**: `spec.md` and `architecture.md`

---

## Executive Summary

This plan outlines the phased implementation of the Phase II Full-Stack Todo Web Application, transforming the Phase I console app into a modern, multi-user web application with authentication, persistent storage, and user-isolated task management.

**Key Architectural Decisions:**
- **Auth**: JWT with short-lived access tokens (15-60 min) + refresh tokens (7-30 days)
- **Security**: Backend-enforced user data isolation (authoritative layer)
- **Concurrency**: Optimistic locking with HTTP 409 Conflict response
- **API**: Full object responses for consistency
- **Workflow**: Spec-driven development with best practices applied to implementation

---

## Development Phases

### Phase 0: Project Setup & Infrastructure

**Objective**: Establish monorepo structure, development environment, and database connection.

**Tasks**:

1. **Monorepo Structure Setup**
   - Create `frontend/` and `backend/` directories
   - Setup root-level package management
   - Configure shared TypeScript types
   - Setup environment variable management

2. **Backend Initialization**
   - Initialize FastAPI project structure
   - Setup Python virtual environment
   - Install dependencies: FastAPI, SQLModel, python-jose, psycopg2, uvicorn
   - Create `.env` template file
   - Setup database connection module

3. **Frontend Initialization**
   - Create Next.js 16+ project with App Router
   - Install dependencies: Better Auth, Tailwind CSS, react-hook-form
   - Setup ESLint and Prettier
   - Configure environment variables
   - Create base layout and routing structure

4. **Database Setup**
   - Create Neon PostgreSQL database
   - Design database schema (users, tasks tables)
   - Create indexes on user_id, completed, created_at
   - Setup connection pooling configuration
   - Create database initialization script

**Deliverables**:
- ✅ Working monorepo structure
- ✅ Backend server starts on localhost:8000
- ✅ Frontend dev server starts on localhost:3000
- ✅ Database connection successful
- ✅ Health check endpoint responds

**Acceptance Criteria**:
- Backend `GET /api/v1/health` returns `{"status": "healthy", "database": "connected"}`
- Frontend loads without errors at localhost:3000
- Database tables created with proper indexes

**Estimated Time**: 2-3 hours

---

### Phase 1: Authentication System (P1)

**Objective**: Implement user registration, login, JWT token management, and refresh token flow.

**Backend Tasks**:

1. **User Model & Schema**
   - Create Better Auth compatible user model (SQLModel)
   - Define user table schema (id, email, password_hash, name, created_at)
   - Implement password hashing with bcrypt
   - Create user CRUD operations

2. **JWT Token Management**
   - Implement JWT generation with HS256 algorithm
   - Create access token (15-60 min expiration)
   - Create refresh token (7-30 day expiration)
   - Setup JWT_SECRET environment variable
   - Implement token validation middleware

3. **Auth Endpoints**
   - `POST /api/v1/auth/signup` - User registration
     - Validate email format
     - Enforce password strength (8+ chars, mixed case, number, special char)
     - Hash password before storage
     - Return user object + tokens
     - Handle duplicate email error

   - `POST /api/v1/auth/login` - User authentication
     - Verify credentials
     - Issue access + refresh tokens
     - Rate limit: 5 failed attempts per 15 min per IP
     - Handle invalid credentials

   - `POST /api/v1/auth/refresh` - Token refresh
     - Validate refresh token
     - Issue new access token
     - Return new token pair

   - `POST /api/v1/auth/logout` - Logout
     - Invalidate refresh token
     - Clear tokens from client

**Frontend Tasks**:

1. **Better Auth Configuration**
   - Setup Better Auth client
   - Configure JWT settings
   - Create auth utilities (useSession, useAuth)
   - Setup token storage (access in memory, refresh in httpOnly cookie)

2. **Auth Pages**
   - Create `/signup` page with form
     - Email input with validation
     - Password input with strength indicator
     - Confirm password field
     - Name field (optional)
     - Submit button with loading state
     - Error display
     - Link to login page

   - Create `/login` page with form
     - Email input
     - Password input with show/hide toggle
     - Remember me checkbox
     - Submit button with loading state
     - Error display
     - Link to signup page

   - Create auth layout with centered card design

3. **Auth State Management**
   - Implement session persistence across page refreshes
   - Handle token expiration and automatic refresh
   - Redirect unauthenticated users to login
   - Implement logout functionality

**Deliverables**:
- ✅ Users can signup with email/password
- ✅ Users can login with valid credentials
- ✅ Invalid credentials show clear error
- ✅ JWT tokens issued and stored correctly
- ✅ Token refresh works automatically
- ✅ Login persists across browser refresh
- ✅ Logout clears session

**Acceptance Criteria**:
- User registration creates account in database
- Login returns access + refresh tokens
- Protected routes redirect to login when unauthenticated
- Access token expires after 15-60 minutes
- Refresh token successfully obtains new access token
- Rate limiting blocks after 5 failed login attempts

**Estimated Time**: 4-5 hours

---

### Phase 2: Task CRUD Operations (P1)

**Objective**: Implement core task management features - create, read, update, delete tasks with user isolation.

**Backend Tasks**:

1. **Task Model & Database**
   - Create Task SQLModel (id, user_id, title, description, completed, created_at, updated_at)
   - Implement foreign key constraint (user_id → users.id)
   - Add database indexes (user_id, completed, created_at DESC)
   - Create task CRUD operations with user scoping

2. **Task CRUD Endpoints**

   - `GET /api/v1/tasks` - List user's tasks
     - Extract user_id from JWT
     - Query: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
     - Return full task objects with all fields
     - Handle empty list gracefully

   - `POST /api/v1/tasks` - Create task
     - Validate title (1-200 chars, not empty/whitespace)
     - Validate description (0-1000 chars, optional)
     - Associate with authenticated user
     - Auto-generate id and timestamps
     - Return created task object (201 status)

   - `GET /api/v1/tasks/{id}` - Get specific task
     - Validate user owns task (WHERE id = ? AND user_id = ?)
     - Return 404 if not found or doesn't belong to user
     - Return full task object

   - `PUT /api/v1/tasks/{id}` - Update task
     - **Optimistic locking**: Check updated_at timestamp
     - Return 409 Conflict if concurrent modification detected
     - Validate title and description constraints
     - Update only if user owns task
     - Auto-update updated_at timestamp
     - Return updated task object (200 status)
     - Return 404 if task not found or doesn't belong to user

   - `DELETE /api/v1/tasks/{id}` - Delete task
     - Verify user owns task
     - Delete from database
     - Return 204 No Content on success
     - Return 404 if task not found or doesn't belong to user

3. **Validation & Error Handling**
   - Pydantic models for request/response validation
   - Custom error handlers for 400, 401, 403, 404, 409, 500
   - Descriptive error messages with error codes
   - Input sanitization to prevent injection

**Frontend Tasks**:

1. **API Client**
   - Create centralized API client (`lib/api.ts`)
   - Implement JWT injection in Authorization header
   - Handle token refresh on 401 responses
   - Type definitions for Task model
   - Error handling utilities

2. **Dashboard Page** (`/dashboard`)
   - Task list component
     - Display tasks in reverse chronological order
     - Show title, description, completion status
     - Visual distinction for completed tasks (strikethrough/color)
     - Loading states
     - Error display
     - Empty state when no tasks

   - Create task button → opens modal/form

   - Statistics summary (completed count, pending count)

3. **Task Form Component**
   - Title input (required, 1-200 chars)
   - Description textarea (optional, 0-1000 chars)
   - Character counters
   - Validation error display
   - Submit button with loading state
   - Cancel button

4. **Task Detail Page** (`/tasks/{id}`)
   - Display all task fields
   - Edit button → opens edit form
   - Delete button with confirmation
   - Toggle completion button
   - Back to dashboard link
   - Loading and error states

5. **Task Operations**
   - Create task from form
   - Edit task with pre-populated form
   - Delete task with confirmation dialog
   - Toggle completion status
   - Handle HTTP 409 Conflict: fetch latest and prompt retry
   - Optimistic UI updates

**Deliverables**:
- ✅ Users can create tasks with title and optional description
- ✅ Task list displays only user's own tasks
- ✅ Users can view task details
- ✅ Users can edit task title and description
- ✅ Users can delete tasks
- ✅ Tasks display in reverse chronological order
- ✅ Concurrent edits handled gracefully (409 → retry)

**Acceptance Criteria**:
- All CRUD operations work correctly
- User isolation enforced (cannot access other users' tasks)
- Validation prevents invalid data (empty titles, length limits)
- Full task objects returned from all endpoints
- Optimistic locking prevents concurrent edit conflicts
- Statistics accurately reflect task counts

**Estimated Time**: 5-6 hours

---

### Phase 3: Task Completion Toggle (P2)

**Objective**: Implement task completion status toggle with visual feedback.

**Backend Tasks**:

1. **Completion Toggle Endpoint**
   - `PATCH /api/v1/tasks/{id}/complete` - Toggle completion
     - Verify user owns task
     - Toggle completed boolean (true ↔ false)
     - Auto-update updated_at timestamp
     - Return updated task object
     - Return 404 if task not found or doesn't belong to user

**Frontend Tasks**:

1. **Completion Toggle Component**
   - Checkbox or button for each task
   - Visual feedback (checkmark icon, strikethrough, color change)
   - Immediate UI update (optimistic)
   - Revert on API error
   - Sync across multiple browser tabs

2. **Filter Views**
   - "All Tasks" (default)
   - "Completed Only" filter
   - "Pending Only" filter
   - Update statistics based on current view

**Deliverables**:
- ✅ Users can mark tasks as complete/incomplete
- ✅ Visual distinction between completed and pending tasks
- ✅ Completion status persists across sessions
- ✅ Filter views work correctly
- ✅ Statistics update to reflect completion status

**Acceptance Criteria**:
- Toggle button correctly switches completion status
- Visual state matches database state
- Filters correctly show completed/pending tasks
- Multiple tabs stay in sync (or handle conflicts gracefully)

**Estimated Time**: 2-3 hours

---

### Phase 4: Security & Validation (P2)

**Objective**: Harden security, implement comprehensive validation, and add error handling.

**Backend Tasks**:

1. **JWT Security Hardening**
   - Verify token signature on every request
   - Check token expiration
   - Extract user_id and attach to request.state
   - Return 401 for missing/invalid tokens
   - Return 403 for cross-user access attempts
   - Log all security events (failed auth, authorization failures)

2. **Input Validation**
   - Server-side validation for all inputs
   - Title: not empty, not whitespace-only, 1-200 chars
   - Description: 0-1000 chars
   - Email: RFC 5322 compliant regex
   - Password: 8+ chars, uppercase, lowercase, number, special char
   - Sanitize inputs to prevent XSS/injection

3. **Error Handling**
   - Custom exception handlers for all error types
   - Consistent error response format:
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
   - Never expose sensitive data in errors (passwords, tokens, stack traces)
   - Proper HTTP status codes (200, 201, 400, 401, 403, 404, 409, 500)

4. **Rate Limiting**
   - 5 failed login attempts per 15 min per IP
   - Implement in-memory storage (Redis if needed later)
   - Return 429 Too Many Requests when rate limited
   - Log rate limit violations

**Frontend Tasks**:

1. **Form Validation**
   - Client-side validation matching backend rules
   - Real-time feedback (character counts, format errors)
   - Display inline error messages
   - Disable submit button until valid
   - Show loading state during submission

2. **Error Display**
   - Toast notifications for API errors
   - Inline validation errors for forms
   - User-friendly error messages
   - Retry mechanism for failed requests
   - Network error handling

3. **Security Best Practices**
   - Never store tokens in localStorage (use httpOnly cookies)
   - Implement CSRF protection (SameSite cookies)
   - Clear tokens on logout
   - Redirect to login on 401 responses
   - Auto-refresh tokens before expiration

**Deliverables**:
- ✅ All endpoints protected with JWT
- ✅ Input validation prevents invalid data
- ✅ Errors handled gracefully with user-friendly messages
- ✅ Rate limiting prevents brute force attacks
- ✅ Sensitive information never exposed in errors

**Acceptance Criteria**:
- Unauthorized requests return 401
- Cross-user access attempts return 403/404
- Invalid inputs return 400 with clear error messages
- Rate limiting blocks after 5 failed logins
- All error messages are user-friendly

**Estimated Time**: 3-4 hours

---

### Phase 5: UI Polish & Responsiveness (P2)

**Objective**: Complete UI implementation with responsive design and accessibility.

**Frontend Tasks**:

1. **Responsive Design**
   - Mobile (320px-767px):
     - Single column layout
     - Hamburger menu (if needed)
     - Touch-friendly buttons (min 44x44px)
     - Full-width forms
     - Simplified task cards

   - Tablet (768px-1023px):
     - Two-column layout for desktop
     - Medium-sized task cards
     - Optimized spacing

   - Desktop (1024px+):
     - Full dashboard layout
     - Sidebar navigation (if applicable)
     - Large task cards with all details visible

2. **Loading States**
   - Skeleton screens for task list
   - Spinners for form submissions
   - Progress indicators for long operations
   - Optimistic UI updates for better perceived performance

3. **Notifications**
   - Success toasts (task created, updated, deleted)
   - Error toasts (API failures, validation errors)
   - Info messages (token refresh, logout)
   - Dismissible after 5 seconds

4. **Accessibility**
   - Semantic HTML (nav, main, section, article)
   - ARIA labels for interactive elements
   - Keyboard navigation support
   - Focus indicators
   - Screen reader compatibility
   - Color contrast ratios (WCAG AA)

5. **Visual Polish**
   - Consistent color scheme
   - Hover states for buttons
   - Smooth transitions
   - Empty state illustrations
   - Error state designs
   - Professional typography

**Deliverables**:
- ✅ Responsive layout works on mobile, tablet, desktop
- ✅ All pages accessible via keyboard
- ✅ Loading states provide good UX
- ✅ Notifications inform users of actions
- ✅ Professional, polished appearance

**Acceptance Criteria**:
- Mobile view passes all responsive tests
- Keyboard navigation works without mouse
- Screen readers can announce all elements
- Color contrast meets WCAG AA standards
- Loading states display within 200ms

**Estimated Time**: 4-5 hours

---

### Phase 6: Testing & Quality Assurance

**Objective**: Comprehensive testing across all features to ensure quality and correctness.

**Backend Testing**:

1. **Unit Tests**
   - Password hashing function
   - JWT generation/validation
   - User ID extraction
   - Task model validation
   - Input sanitization

2. **Integration Tests**
   - Auth endpoints (signup, login, refresh, logout)
   - Task CRUD endpoints
   - JWT middleware
   - User isolation enforcement
   - Optimistic locking
   - Rate limiting
   - Error handling

3. **API Contract Tests**
   - Verify response formats match spec
   - Check HTTP status codes
   - Validate error response structures
   - Test full object returns

**Frontend Testing**:

1. **Unit Tests**
   - Form validation logic
   - Utility functions
   - API client methods
   - Auth state management

2. **Component Tests**
   - Task list rendering
   - Task form validation
   - Completion toggle
   - Error display components
   - Navigation components

3. **Integration Tests**
   - Auth flows (signup → login → dashboard)
   - Task creation flow
   - Task update flow
   - Task deletion flow
   - Token refresh flow

4. **E2E Tests (Playwright)**
   - Complete signup and login flow
   - Create task from form
   - Edit task details
   - Toggle completion status
   - Delete task with confirmation
   - Logout flow
   - Protected route redirects

**Security Testing**:

1. **Authentication Tests**
   - Verify JWT required on all protected endpoints
   - Test invalid token rejection
   - Test expired token rejection
   - Test token refresh works

2. **Authorization Tests**
   - Verify user cannot access other users' tasks
   - Test 404/403 responses for cross-user access
   - Verify user isolation on all endpoints

3. **Input Validation Tests**
   - SQL injection attempts
   - XSS attempts in task fields
   - Path traversal attempts
   - Invalid email formats
   - Weak password rejection

4. **Concurrency Tests**
   - Two tabs updating same task simultaneously
   - Verify HTTP 409 Conflict returned
   - Verify client handles conflict correctly

**Performance Testing**:

1. **Load Tests**
   - 100 concurrent users (SC-003)
   - Measure API response times (target <300ms p95)
   - Database query performance
   - Connection pool exhaustion handling

2. **Stress Tests**
   - Maximum tasks per user
   - Large description handling
   - Rapid task creation/deletion

**Deliverables**:
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ All E2E tests pass
- ✅ Security tests pass (no vulnerabilities)
- ✅ Performance targets met (SC-003, SC-004)
- ✅ Test coverage >80% for backend, >70% for frontend

**Acceptance Criteria**:
- Test suite runs successfully
- All user stories pass acceptance tests
- No critical security vulnerabilities
- API response times <300ms (p95)
- 100 concurrent users supported without degradation

**Estimated Time**: 6-8 hours

---

## Testing Strategy

### Unit Testing

**Backend (pytest)**:
- Test individual functions in isolation
- Mock database dependencies
- Test edge cases and error conditions
- Coverage goal: >80%

**Frontend (Vitest)**:
- Test utility functions
- Test React components in isolation
- Mock API calls
- Coverage goal: >70%

### Integration Testing

**Backend API Tests**:
- Test each endpoint with valid/invalid inputs
- Test authentication/authorization
- Test user isolation
- Test error responses
- Test database operations

**Frontend Integration Tests**:
- Test component interactions
- Test API client integration
- Test state management
- Test navigation flows

### End-to-End Testing

**E2E (Playwright)**:
- Test complete user journeys
- Test authentication flow
- Test task CRUD operations
- Test error scenarios
- Test responsive design

### Security Testing

**Security Tests**:
- Test authentication bypasses
- Test authorization bypasses
- Test input validation (SQL injection, XSS)
- Test rate limiting
- Test token security

### Performance Testing

**Load Tests (locust)**:
- Simulate 100 concurrent users
- Measure API response times
- Identify bottlenecks
- Verify SC-003, SC-004

---

## Quality Validation Checklist

### Functional Requirements

- [ ] FR-001: User signup with email/password
- [ ] FR-002: Email format validation
- [ ] FR-003: Password strength enforcement
- [ ] FR-004: Password hashing with bcrypt
- [ ] FR-005: Duplicate email prevention
- [ ] FR-006: Login issues JWT tokens
- [ ] FR-007: JWT includes user_id and expiration
- [ ] FR-008: Access token expires 15-60 min
- [ ] FR-009: Refresh token endpoint works
- [ ] FR-010: Logout clears session
- [ ] FR-011: Login rate limiting (5/15min)
- [ ] FR-012-FR-029: Task CRUD operations
- [ ] FR-030-FR-036: API security requirements
- [ ] FR-037-FR-041: Data persistence requirements
- [ ] FR-042-FR-051: User interface requirements
- [ ] FR-052-FR-057: Error handling requirements

### Security Requirements

- [ ] All endpoints require JWT (except auth)
- [ ] Backend enforces user data isolation
- [ ] Passwords hashed before storage
- [ ] JWT tokens verified on every request
- [ ] Rate limiting on login endpoint
- [ ] Input validation on all endpoints
- [ ] SQL injection prevented
- [ ] XSS prevented
- [ ] CSRF protection enabled
- [ ] Optimistic locking prevents concurrent edit conflicts

### Performance Requirements

- [ ] API response <300ms (p95) for CRUD
- [ ] Supports 100 concurrent users
- [ ] Database queries properly indexed
- [ ] Connection pooling configured
- [ ] Frontend loads within 3 seconds

### User Experience Requirements

- [ ] Forms provide inline validation
- [ ] Loading states displayed during operations
- [ ] Success/error notifications shown
- [ ] Responsive on mobile/tablet/desktop
- [ ] Keyboard navigation works
- [ ] Empty states handled gracefully

---

## Risk Mitigation

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Better Auth compatibility with FastAPI** | High | Use shared JWT_SECRET; implement custom verification middleware if needed |
| **JWT refresh token management complexity** | Medium | Document refresh flow clearly; implement client-side auto-refresh |
| **Optimistic locking conflicts** | Medium | Provide clear user guidance on 409 responses; auto-retry option |
| **Database connection exhaustion** | Medium | Configure connection pooling; implement retry logic |
| **Frontend-backend integration issues** | Low | Define clear API contract; use TypeScript types |

### Development Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Time constraints (hackathon)** | High | Follow phased approach; prioritize P1 features first |
| **Spec ambiguity** | Medium | Run `/sp.clarify` before planning (completed) |
| **Testing coverage gaps** | Medium | Allocate dedicated testing phase; automate where possible |
| **Environment setup issues** | Low | Document setup process; use Docker if needed |

---

## Success Metrics

### Phase Completion Criteria

Each phase is considered complete when:
- ✅ All tasks implemented
- ✅ All acceptance criteria met
- ✅ All tests passing
- ✅ Code reviewed against spec
- ✅ Documentation updated

### Overall Success Criteria (from spec.md)

- **SC-001**: Registration/login flow <90 seconds ✅
- **SC-002**: Create task <10 seconds ✅
- **SC-003**: 100 concurrent users without degradation ✅
- **SC-004**: 95% API responses <300ms ✅
- **SC-005**: 100% user isolation enforced ✅
- **SC-006**: Basic workflows work on first attempt ✅
- **SC-007**: Connection pool exhaustion handled ✅
- **SC-008**: Zero security vulnerabilities ✅
- **SC-009**: All inputs validated/sanitized ✅
- **SC-010**: Responsive design passes all tests ✅
- **SC-011**: Data persists across sessions ✅
- **SC-012**: User satisfaction with interface ✅

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Run `/sp.tasks`** to generate detailed task breakdown
3. **Begin Phase 0** - Project setup
4. **Track progress** with regular checkpoints
5. **Adjust timeline** as needed based on velocity

---

**Document Status**: ✅ Ready for Implementation
**Last Updated**: January 17, 2026
**Phase**: Phase II - Full-Stack Web Application
