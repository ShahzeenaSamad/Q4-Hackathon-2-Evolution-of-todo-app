# Tasks: Full-Stack Todo Web Application (Phase II)

**Feature Branch**: `phase-2-web`
**Created**: 2026-01-17
**Prerequisites**: spec.md (user stories), plan.md (implementation phases), specs/architecture.md (technical decisions)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo structure**: `backend/` for FastAPI backend, `frontend/` for Next.js frontend
- Tests are OPTIONAL - only included if explicitly requested for validation

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure establishment

- [x] T001 Create monorepo root structure with backend/ and frontend/ directories at repository root
- [x] T002 [P] Create root-level package.json with shared scripts and workspace configuration
- [x] T003 [P] Create .gitignore for node_modules, __pycache__, .env, *.pyc, .venv
- [x] T004 [P] Create root .env.example template with DATABASE_URL, JWT_SECRET, BETTER_AUTH_SECRET placeholders
- [x] T005 [P] Create README.md with project overview, setup instructions, and architecture diagram

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T006 Initialize Python project in backend/ with pyproject.toml and requirements.txt
- [ ] T007 [P] Install FastAPI dependencies: fastapi, uvicorn, sqlmodel, psycopg2-binary, python-jose[cryptography], passlib[bcrypt], python-multipart
- [ ] T008 [P] Setup Python virtual environment in backend/.venv
- [ ] T009 [P] Create backend/.env template from root .env.example
- [ ] T010 Create backend/main.py with FastAPI app instance, CORS middleware, and versioned API router (/api/v1)
- [ ] T011 [P] Create backend/db.py with database connection pool, SQLModel session management, and Neon PostgreSQL configuration
- [ ] T012 [P] Implement health check endpoint GET /api/v1/health in backend/main.py returning database connection status

### Frontend Foundation

- [ ] T013 Initialize Next.js 16+ project in frontend/ with App Router using `npx create-next-app@latest`
- [ ] T014 [P] Install frontend dependencies: better-auth, @auth/prisma-adapter, tailwindcss, react-hook-form, zod
- [ ] T015 [P] Configure Tailwind CSS in frontend/tailwind.config.js and frontend/app/globals.css
- [ ] T016 [P] Setup ESLint and Prettier in frontend/.eslintrc.json and frontend/.prettierrc
- [ ] T017 [P] Create frontend/.env.local template with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET placeholders
- [ ] T018 Create frontend/lib/types.ts with shared TypeScript types for User and Task entities

### Database Foundation

- [ ] T019 Create database schema in backend/init_db.py with users and tasks tables matching Better Auth compatibility
- [ ] T020 [P] Create indexes on tasks table: idx_tasks_user_id, idx_tasks_completed, idx_tasks_created_at DESC
- [ ] T021 [P] Setup foreign key constraint: tasks.user_id REFERENCES users(id) ON DELETE CASCADE
- [ ] T022 Run database initialization script and verify tables created in Neon PostgreSQL

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to signup, login, and maintain secure sessions with JWT token management

**Independent Test**: Register a new user, logout, and login again to verify session creation and authentication flow

### Backend: User Model & Authentication

- [ ] T023 [P] [US1] Create User SQLModel in backend/models/user.py with id (TEXT), email (TEXT, unique), password_hash (TEXT), name (TEXT), created_at (TIMESTAMP)
- [ ] T024 [P] [US1] Implement password hashing function in backend/auth/security.py using bcrypt with salt rounds=10
- [ ] T025 [P] [US1] Create JWT utility functions in backend/auth/jwt.py: create_access_token(), create_refresh_token(), decode_token(), verify_token()
- [ ] T026 [P] [US1] Implement JWT validation middleware in backend/auth/middleware.py that extracts token from Authorization header, verifies signature, and attaches user_id to request.state
- [ ] T027 [US1] Implement rate limiting decorator in backend/auth/rate_limiter.py using in-memory storage (5 attempts per 15 min per IP)
- [ ] T028 [US1] Create user CRUD service in backend/services/user_service.py with create_user(), get_user_by_email(), verify_credentials()

### Backend: Auth Endpoints

- [ ] T029 [US1] Implement POST /api/v1/auth/signup endpoint in backend/routes/auth.py with email validation, password strength check, password hashing, and user creation
- [ ] T030 [US1] Implement POST /api/v1/auth/login endpoint in backend/routes/auth.py with credential verification, rate limiting, JWT token generation (access + refresh), and token return
- [ ] T031 [US1] Implement POST /api/v1/auth/refresh endpoint in backend/routes/auth.py with refresh token validation and new access token issuance
- [ ] T032 [US1] Implement POST /api/v1/auth/logout endpoint in backend/routes/auth.py with refresh token invalidation
- [ ] T033 [US1] Register auth routes in backend/main.py under /api/v1/auth prefix

### Frontend: Better Auth Configuration

- [ ] T034 [P] [US1] Create Better Auth client configuration in frontend/lib/auth.ts with database adapter, email/password enabled, JWT settings (expiresIn: "15m", refreshAge: "7d")
- [ ] T035 [P] [US1] Create auth utility hooks in frontend/lib/auth.ts: useSession(), useAuth() for accessing session state and auth methods
- [ ] T036 [P] [US1] Setup token storage: access tokens in memory, refresh tokens in httpOnly cookies via Better Auth configuration

### Frontend: Auth Pages

- [ ] T037 [US1] Create frontend/app/(auth)/layout.tsx with centered card layout and app branding
- [ ] T038 [US1] Create frontend/app/(auth)/signup/page.tsx with signup form: email input (validation), password input (strength indicator), confirm password field, name field (optional), submit button with loading state, error display, link to login
- [ ] T039 [US1] Create frontend/app/(auth)/login/page.tsx with login form: email input, password input with show/hide toggle, remember me checkbox, submit button with loading state, error display, link to signup
- [ ] T040 [US1] Implement form validation in signup and login pages using react-hook-form with Zod schemas matching backend rules
- [ ] T041 [US1] Implement redirect after successful signup to /login and after successful login to /dashboard

### Frontend: Auth State Management

- [ ] T042 [US1] Implement session persistence across page refreshes in frontend/lib/auth.ts by checking Better Auth session on mount
- [ ] T043 [US1] Implement automatic token refresh before expiration in frontend/lib/auth.ts using Better Auth refresh mechanism
- [ ] T044 [US1] Create protected route wrapper in frontend/components/auth-guard.tsx that redirects to /login if session not found
- [ ] T045 [US1] Implement logout functionality in frontend/lib/auth.ts with Better Auth signOut() and redirect to /login

**Checkpoint**: User can signup, login, maintain session across refresh, and logout - authentication MVP complete!

---

## Phase 4: User Story 2 - Create and View Personal Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create tasks with titles/descriptions and view their task list

**Independent Test**: Login, create a task, and immediately see it in the task list to confirm data persistence

### Backend: Task Model

- [ ] T046 [P] [US2] Create Task SQLModel in backend/models/task.py with id (SERIAL), user_id (TEXT FK), title (VARCHAR 200), description (TEXT), completed (BOOLEAN), created_at (TIMESTAMP), updated_at (TIMESTAMP)
- [ ] T047 [P] [US2] Add database indexes in backend/init_db.py if not already created: idx_tasks_user_id, idx_tasks_completed, idx_tasks_created_at DESC
- [ ] T048 [US2] Create task CRUD service in backend/services/task_service.py with create_task(), get_user_tasks(), get_task_by_id(), ensuring all queries scoped by user_id

### Backend: Task CRUD Endpoints

- [ ] T049 [US2] Implement GET /api/v1/tasks endpoint in backend/routes/tasks.py that extracts user_id from JWT, queries tasks WHERE user_id = ? ORDER BY created_at DESC, and returns full task objects
- [ ] T050 [US2] Implement POST /api/v1/tasks endpoint in backend/routes/tasks.py with title validation (1-200 chars, not empty/whitespace), description validation (0-1000 chars), user association, auto-generated timestamps, and returns created task (201 status)
- [ ] T051 [US2] Implement GET /api/v1/tasks/{id} endpoint in backend/routes/tasks.py that validates user owns task (WHERE id = ? AND user_id = ?), returns 404 if not found or doesn't belong to user, returns full task object
- [ ] T052 [US2] Register task routes in backend/main.py under /api/v1/tasks prefix with JWT middleware dependency
- [ ] T053 [US2] Add optimistic locking check using updated_at timestamp for all update operations (return 409 Conflict if modified since client fetch)

### Frontend: API Client

- [ ] T054 [P] [US2] Create centralized API client in frontend/lib/api.ts with base URL configuration, JWT token injection in Authorization header, 401 auto-refresh handling, and typed response methods
- [ ] T055 [P] [US2] Create Task type definition in frontend/lib/types.ts matching backend Task model
- [ ] T056 [P] [US2] Implement error handling utilities in frontend/lib/api.ts for consistent error display (400 validation, 401 unauthorized, 403 forbidden, 404 not found, 409 conflict)

### Frontend: Dashboard & Task List

- [ ] T057 [US2] Create frontend/app/dashboard/page.tsx with protected route wrapper, task list display, and loading states
- [ ] T058 [US2] Create TaskList component in frontend/components/tasks/task-list.tsx that fetches tasks from API, displays tasks in reverse chronological order, shows visual distinction for completed tasks, and handles empty state
- [ ] T059 [US2] Create TaskCard component in frontend/components/tasks/task-card.tsx displaying title, description (truncated), completion status with checkbox, created_at timestamp, edit button, and delete button
- [ ] T060 [US2] Implement task fetching in frontend/app/dashboard/page.tsx using useEffect on mount, with loading spinner and error display
- [ ] T061 [US2] Create TaskStatistics component in frontend/components/tasks/task-statistics.tsx showing completed count and pending count

### Frontend: Task Creation Form

- [ ] T062 [US2] Create CreateTaskForm component in frontend/components/tasks/create-task-form.tsx with title input (required, 1-200 chars, character counter), description textarea (optional, 0-1000 chars, character counter), validation error display, submit button with loading state, cancel button
- [ ] T063 [US2] Implement form validation in CreateTaskForm using react-hook-form with Zod schema: title min 1 max 200 chars, not whitespace-only; description max 1000 chars
- [ ] T064 [US2] Integrate CreateTaskForm in frontend/app/dashboard/page.tsx with modal or inline form, optimistic UI update on submit, error display, and task list refresh on success

**Checkpoint**: User can create tasks and view them in the task list - core CRUD functionality working!

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Enable users to edit task title and description with validation and concurrent edit handling

**Independent Test**: Create a task, edit title and description, save changes, and verify updates persist correctly

### Backend: Update Endpoint

- [ ] T065 [US3] Implement PUT /api/v1/tasks/{id} endpoint in backend/routes/tasks.py with optimistic locking (check updated_at timestamp matches request), title validation (1-200 chars, not empty), description validation (0-1000 chars), auto-update updated_at, return 409 Conflict if concurrent modification detected
- [ ] T066 [US3] Add update_task() method to backend/services/task_service.py that updates task only if user owns it and returns updated task or None

### Frontend: Edit Task Form

- [ ] T067 [US3] Create EditTaskForm component in frontend/components/tasks/edit-task-form.tsx with pre-populated title and description fields, character counters, validation error display, submit button with loading state, cancel button
- [ ] T068 [US3] Implement form validation in EditTaskForm using react-hook-form with same Zod schema as CreateTaskForm
- [ ] T069 [US3] Create TaskDetailPage in frontend/app/tasks/[id]/page.tsx displaying full task information (title, description, completion status, created_at, updated_at timestamps), edit button, delete button, and back to dashboard link
- [ ] T070 [US3] Integrate EditTaskForm in TaskDetailPage with modal or inline form, optimistic UI update, error display, and redirect to dashboard on success
- [ ] T071 [US3] Handle HTTP 409 Conflict response in frontend/lib/api.ts by fetching latest task state and prompting user to retry or overwrite

**Checkpoint**: User can edit task details and system handles concurrent edit conflicts - task updates working!

---

## Phase 6: User Story 4 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status with visual feedback and filtering

**Independent Test**: Create tasks, mark as complete, verify visual change, then mark as incomplete to toggle status

### Backend: Toggle Completion Endpoint

- [ ] T072 [US4] Implement PATCH /api/v1/tasks/{id}/complete endpoint in backend/routes/tasks.py that validates user owns task, toggles completed boolean (true ↔ false), auto-updates updated_at, and returns updated task object

### Frontend: Completion Toggle & Filtering

- [ ] T073 [US4] Add completion toggle button/checkbox to TaskCard component in frontend/components/tasks/task-card.tsx with immediate visual feedback (checkmark icon, strikethrough text, color change)
- [ ] T074 [US4] Implement optimistic UI update in TaskCard for completion toggle with automatic rollback on API error
- [ ] T075 [US4] Create TaskFilters component in frontend/components/tasks/task-filters.tsx with "All Tasks", "Completed Only", "Pending Only" filter buttons
- [ ] T076 [US4] Implement filter logic in TaskList component to show/hide tasks based on completion status when filter selected
- [ ] T077 [US4] Update TaskStatistics component to reflect current view statistics (showing completed/pending count based on active filter)

**Checkpoint**: User can toggle completion status and filter tasks - task completion tracking working!

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Enable users to permanently delete tasks with confirmation

**Independent Test**: Create a task, delete it with confirmation, and verify it no longer appears in any view

### Backend: Delete Endpoint

- [ ] T078 [US5] Implement DELETE /api/v1/tasks/{id} endpoint in backend/routes/tasks.py that validates user owns task, deletes from database, and returns 204 No Content
- [ ] T079 [US5] Add delete_task() method to backend/services/task_service.py that deletes task only if user owns it and returns True/False

### Frontend: Delete Confirmation

- [ ] T080 [US5] Add delete button to TaskCard component with confirmation prompt ("Are you sure you want to delete this task?")
- [ ] T081 [US5] Add delete button to TaskDetailPage in frontend/app/tasks/[id]/page.tsx with same confirmation prompt
- [ ] T082 [US5] Implement delete functionality in frontend/lib/api.ts with optimistic removal from UI on confirm, rollback on error, and task list refresh
- [ ] T083 [US5] Update TaskStatistics component to decrement completed count when completed task is deleted

**Checkpoint**: User can delete tasks with confirmation - task deletion working!

---

## Phase 8: User Story 6 - View Individual Task Details (Priority: P3)

**Goal**: Provide dedicated detail page for viewing full task information

**Independent Test**: Click on a task from the list, view all details, and return to the list

### Frontend: Task Detail Page Enhancement

- [ ] T084 [US6] Enhance TaskDetailPage in frontend/app/tasks/[id]/page.tsx to handle empty description case with placeholder text ("No description provided")
- [ ] T085 [US6] Add "Back to Dashboard" button/link to TaskDetailPage for navigation back to task list
- [ ] T086 [US6] Implement edit and delete buttons in TaskDetailPage that open EditTaskForm and show delete confirmation respectively

**Checkpoint**: Task detail page provides comprehensive view with all fields - task detail view working!

---

## Phase 9: Security & Validation (Cross-Cutting)

**Purpose**: Harden security, implement comprehensive validation, and ensure user data isolation

### Backend Security Hardening

- [ ] T087 [P] Verify JWT signature and expiration on every protected endpoint in backend/auth/middleware.py with proper error responses (401 for invalid/expired tokens)
- [ ] T088 [P] Implement backend-enforced user data isolation in backend/services/task_service.py by ensuring ALL database queries include WHERE user_id = ? clause
- [ ] T089 [P] Add server-side input validation using Pydantic models in backend/schemas/task.py with TaskCreate, TaskUpdate schemas enforcing title (1-200 chars, not empty/whitespace) and description (0-1000 chars)
- [ ] T090 [P] Implement custom exception handlers in backend/main.py for 400 (validation), 401 (unauthorized), 403 (forbidden), 404 (not found), 409 (conflict), 500 (server error) with consistent error response format
- [ ] T091 [P] Sanitize user inputs in backend/services/task_service.py to prevent SQL injection and XSS attacks (SQLModel parameterized queries handle SQL injection)
- [ ] T092 [P] Log all security events in backend/main.py: failed authentication, authorization failures, rate limit violations, with user_id and timestamp context
- [ ] T093 [P] Implement rate limiting for login endpoint in backend/routes/auth.py using decorator from T027 (5 attempts per 15 min per IP)

### Frontend Security & Validation

- [ ] T094 [P] Implement client-side validation matching backend rules in frontend/lib/validation.ts with Zod schemas for TaskCreate and TaskUpdate
- [ ] T095 [P] Add inline validation error display to all forms (CreateTaskForm, EditTaskForm) showing specific field errors
- [ ] T096 [P] Disable submit buttons in all forms until validation passes using react-hook-form formState.isValid
- [ ] T097 [P] Show loading states during form submissions in all forms with spinner or button text change
- [ ] T098 [P] Display toast notifications for API success responses in frontend/components/ui/toast.tsx for task created/updated/deleted
- [ ] T099 [P] Display toast notifications for API errors in frontend/components/ui/toast.tsx with user-friendly error messages and retry mechanism
- [ ] T100 [P] Implement automatic token refresh on 401 responses in frontend/lib/api.ts by calling refresh endpoint and retrying original request
- [ ] T101 [P] Clear tokens from memory and cookies on logout in frontend/lib/auth.ts and redirect to /login

**Checkpoint**: Security and validation hardened across all features - application secure!

---

## Phase 10: UI Polish & Responsiveness (Cross-Cutting)

**Purpose**: Complete UI implementation with responsive design, loading states, and accessibility

### Responsive Design

- [ ] T102 [P] Implement mobile layout (320px-767px) in TaskList component with single column, full-width cards, touch-friendly buttons (min 44x44px)
- [ ] T103 [P] Implement tablet layout (768px-1023px) in TaskList component with two-column layout and medium-sized cards
- [ ] T104 [P] Implement desktop layout (1024px+) in TaskList component with multi-column layout and large cards
- [ ] T105 [P] Apply responsive breakpoints to all forms using Tailwind CSS classes (sm:, md:, lg:, xl:)
- [ ] T106 [P] Test responsive design on all viewport sizes and verify no horizontal scrolling or overlapping elements

### Loading States & Feedback

- [ ] T107 [P] Create loading skeleton component in frontend/components/ui/skeleton.tsx for task list during initial fetch
- [ ] T108 [P] Add loading spinners to all form submit buttons (CreateTaskForm, EditTaskForm, signup, login)
- [ ] T109 [P] Implement optimistic UI updates in TaskCard for completion toggle and deletion with automatic rollback on error
- [ ] T110 [P] Add progress indicators for long-running operations in frontend/components/ui/progress.tsx

### Accessibility

- [ ] T111 [P] Ensure semantic HTML in all components (nav, main, section, article, button, input)
- [ ] T112 [P] Add ARIA labels to all interactive elements in TaskCard and forms (aria-label, aria-describedby)
- [ ] T113 [P] Implement keyboard navigation support (Tab, Enter, Escape) for all buttons and forms
- [ ] T114 [P] Add visible focus indicators to all interactive elements using Tailwind focus:ring classes
- [ ] T115 [P] Verify color contrast ratios meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text)

### Visual Polish

- [ ] T116 [P] Create consistent color scheme in frontend/app/globals.css with CSS variables for primary, secondary, success, error colors
- [ ] T117 [P] Add hover states to all interactive elements (buttons, cards, links) using Tailwind hover: classes
- [ ] T118 [P] Add smooth transitions to all state changes using Tailwind transition-* classes
- [ ] T119 [P] Create empty state illustration in frontend/components/ui/empty-state.tsx for task list when no tasks exist
- [ ] T120 [P] Create error state design in frontend/components/ui/error-state.tsx for API failures
- [ ] T121 [P] Apply professional typography using Tailwind font-* classes with consistent font sizes and weights

**Checkpoint**: UI polished, responsive, and accessible - professional user experience complete!

---

## Phase 11: Testing & Quality Assurance

**Purpose**: Comprehensive testing across all features to ensure quality and correctness

### Backend Testing (pytest)

- [ ] T122 [P] Write unit test for password hashing function in backend/tests/test_auth_security.py
- [ ] T123 [P] Write unit test for JWT generation/validation in backend/tests/test_auth_jwt.py
- [ ] T124 [P] Write unit test for user_id extraction in backend/tests/test_auth_middleware.py
- [ ] T125 [P] Write integration test for POST /api/v1/auth/signup in backend/tests/test_auth_routes.py (valid signup, duplicate email, weak password)
- [ ] T126 [P] Write integration test for POST /api/v1/auth/login in backend/tests/test_auth_routes.py (valid login, invalid credentials, rate limiting)
- [ ] T127 [P] Write integration test for POST /api/v1/auth/refresh in backend/tests/test_auth_routes.py
- [ ] T128 [P] Write integration test for GET /api/v1/tasks in backend/tests/test_task_routes.py (returns only user's tasks, empty list)
- [ ] T129 [P] Write integration test for POST /api/v1/tasks in backend/tests/test_task_routes.py (valid creation, title validation, user association)
- [ ] T130 [P] Write integration test for PUT /api/v1/tasks/{id} in backend/tests/test_task_routes.py (valid update, optimistic locking 409, cross-user 403)
- [ ] T131 [P] Write integration test for DELETE /api/v1/tasks/{id} in backend/tests/test_task_routes.py (valid delete, cross-user 403)
- [ ] T132 [P] Write integration test for PATCH /api/v1/tasks/{id}/complete in backend/tests/test_task_routes.py (toggle completion)
- [ ] T133 [P] Write security test for JWT verification on all protected endpoints in backend/tests/test_security.py
- [ ] T134 [P] Write security test for user isolation enforcement in backend/tests/test_security.py (attempt cross-user access)
- [ ] T135 [P] Write security test for input validation (SQL injection, XSS) in backend/tests/test_security.py

### Frontend Testing (Vitest + Playwright)

- [ ] T136 [P] Write unit test for form validation logic in frontend/lib/validation.test.ts
- [ ] T137 [P] Write unit test for API client methods in frontend/lib/api.test.ts
- [ ] T138 [P] Write component test for TaskList rendering in frontend/components/tasks/task-list.test.tsx
- [ ] T139 [P] Write component test for CreateTaskForm validation in frontend/components/tasks/create-task-form.test.tsx
- [ ] T140 [P] Write E2E test with Playwright for complete signup flow in frontend/e2e/auth.spec.ts (navigate to signup, fill form, submit, verify redirect to login)
- [ ] T141 [P] Write E2E test with Playwright for complete login flow in frontend/e2e/auth.spec.ts (navigate to login, fill form, submit, verify redirect to dashboard)
- [ ] T142 [P] Write E2E test with Playwright for task creation flow in frontend/e2e/tasks.spec.ts (login, create task, verify appears in list)
- [ ] T143 [P] Write E2E test with Playwright for task update flow in frontend/e2e/tasks.spec.ts (login, create task, edit task, save, verify update persists)
- [ ] T144 [P] Write E2E test with Playwright for task completion toggle flow in frontend/e2e/tasks.spec.ts (login, create task, toggle complete, verify visual change)
- [ ] T145 [P] Write E2E test with Playwright for task deletion flow in frontend/e2e/tasks.spec.ts (login, create task, delete, verify removed from list)
- [ ] T146 [P] Write E2E test with Playwright for logout flow in frontend/e2e/auth.spec.ts (login, logout, verify redirect to login, verify protected routes redirect)

### Performance Testing

- [ ] T147 [P] Run load test with 100 concurrent users using locust in locustfile.py and verify no performance degradation (SC-003)
- [ ] T148 [P] Measure API response times and verify 95% of responses complete in under 300ms (SC-004)

**Checkpoint**: All tests passing, security validated, performance targets met - application ready for deployment!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - US1 (Auth) and US2 (Create/View Tasks) are both P1 and can proceed in parallel after Foundation
  - US3-US6 (P2-P3) can proceed in parallel or sequentially after US1 and US2
- **Security & Validation (Phase 9)**: Depends on all user stories being complete
- **UI Polish (Phase 10)**: Can proceed in parallel with Phase 9 after user stories complete
- **Testing (Phase 11)**: Depends on all implementation being complete

### User Story Dependencies

- **US1 (Authentication - P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **US2 (Create/View Tasks - P1)**: Can start after Foundational (Phase 2) - Requires US1 for authentication context but independently testable
- **US3 (Update Tasks - P2)**: Requires US2 (tasks must exist to update)
- **US4 (Completion Toggle - P2)**: Requires US2 (tasks must exist to toggle)
- **US5 (Delete Tasks - P2)**: Requires US2 (tasks must exist to delete)
- **US6 (Task Details - P3)**: Requires US2 (tasks must exist to view details)

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T004, T005)
- All Foundational backend tasks marked [P] can run in parallel (T007, T008, T009, T014, T015, T016)
- All Foundational frontend tasks marked [P] can run in parallel (T020, T021)
- Once Foundational phase completes, US1 (Auth) and US2 (Create/View Tasks) can start in parallel
- All US1 backend models marked [P] can run in parallel (T023, T024, T025, T026)
- All US1 auth pages can run in parallel after backend auth endpoints complete
- US2 frontend API client and components can run in parallel (T054, T055, T056, T057, T058, T059, T060, T061)
- US3-US6 can proceed in parallel after US2 completes (different features, different files)
- All security tasks marked [P] can run in parallel (T087, T088, T089, T090, T091, T092, T093)
- All frontend validation tasks marked [P] can run in parallel (T094, T095, T096, T097, T098, T099)
- All responsive design tasks marked [P] can run in parallel (T102, T103, T104, T105, T106)
- All loading states tasks marked [P] can run in parallel (T107, T108, T109, T110)
- All accessibility tasks marked [P] can run in parallel (T111, T112, T113, T114, T115)
- All visual polish tasks marked [P] can run in parallel (T116, T117, T118, T119, T120, T121)
- All backend tests marked [P] can run in parallel (T122-T136)
- All frontend tests marked [P] can run in parallel (T136-T146)

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch all backend auth models together (after foundation):
Task: "T023 [P] [US1] Create User SQLModel in backend/models/user.py"
Task: "T024 [P] [US1] Implement password hashing function in backend/auth/security.py"
Task: "T025 [P] [US1] Create JWT utility functions in backend/auth/jwt.py"
Task: "T026 [P] [US1] Implement JWT validation middleware in backend/auth/middleware.py"

# Launch all auth tests together (after implementation):
Task: "T125 [P] Write integration test for POST /api/v1/auth/signup"
Task: "T126 [P] Write integration test for POST /api/v1/auth/login"
Task: "T127 [P] Write integration test for POST /api/v1/auth/refresh"

# Launch all auth pages together (after backend endpoints):
Task: "T037 [US1] Create frontend/app/(auth)/layout.tsx"
Task: "T038 [US1] Create frontend/app/(auth)/signup/page.tsx"
Task: "T039 [US1] Create frontend/app/(auth)/login/page.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T022) ⚠️ BLOCKS ALL STORIES
3. Complete Phase 3: User Story 1 - Authentication (T023-T045) 🎯
4. Complete Phase 4: User Story 2 - Create/View Tasks (T046-T064) 🎯
5. **STOP and VALIDATE**: Test authentication and task creation independently
6. Deploy/demo if ready - core MVP working!

### Incremental Delivery (All User Stories)

1. Complete Setup + Foundational (T001-T022) → Foundation ready
2. Add User Story 1 - Authentication (T023-T045) → Test independently → Auth working! 🎯
3. Add User Story 2 - Create/View Tasks (T046-T064) → Test independently → CRUD working! 🎯
4. Add User Story 3 - Update Tasks (T065-T071) → Test independently → Updates working!
5. Add User Story 4 - Completion Toggle (T072-T077) → Test independently → Completion working!
6. Add User Story 5 - Delete Tasks (T078-T083) → Test independently → Deletion working!
7. Add User Story 6 - Task Details (T084-T086) → Test independently → Details working!
8. Add Security & Validation (T087-T101) → Security hardened!
9. Add UI Polish (T102-T121) → Professional UX!
10. Add Testing (T122-T148) → Production ready!

Each user story adds value without breaking previous stories.

### Parallel Team Strategy (Hypothetical Multiple Developers)

With multiple developers after Foundational phase completes:

1. **Developer A**: User Story 1 - Authentication (T023-T045)
2. **Developer B**: User Story 2 - Create/View Tasks (T046-T064)
3. **Developer C**: Begin User Story 3 - Update Tasks (T065-T071) after US2 completes

Stories complete and integrate independently with minimal coordination needed.

---

## Notes

- Total tasks: 148
- Tasks organized by 6 user stories (US1-US6) plus Setup, Foundation, Security, Polish, and Testing phases
- Each user story is independently completable and testable
- [P] marks parallelizable tasks (different files, no dependencies)
- MVP scope: Phases 1-4 (Setup + Foundation + US1 Auth + US2 Create/View) = 64 tasks
- Full implementation: All 11 phases = 148 tasks
- Verify checkpoints after each phase to ensure story independence
- Stop at any checkpoint to validate story independently before proceeding
- All file paths are explicit for immediate execution by LLM
