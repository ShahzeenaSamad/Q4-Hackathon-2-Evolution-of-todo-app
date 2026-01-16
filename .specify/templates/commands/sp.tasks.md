---
description: "Generate task breakdown from feature specification and plan"
---

# Task Generation Command

## Usage
```
/sp.tasks <feature-name>
```

## Description
Generates a detailed, implementable task list based on feature specification and implementation plan.

## Prerequisites
- Feature spec MUST exist: `specs/<feature-name>/spec.md`
- Implementation plan SHOULD exist: `specs/<feature-name>/plan.md`
- Spec MUST have user stories with priorities (P1, P2, P3)

## Task Format
```
[ID] [P?] [Story] Description
```

- **[ID]**: Sequential task number (T001, T002, etc.)
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2, US3)
- **Description**: What to do with file paths

## Task Organization

### Phase 1: Setup (Shared Infrastructure)
Purpose: Project initialization and basic structure

Example tasks:
- T001: Create project structure per implementation plan
- T002: Initialize language project with dependencies
- T003 [P]: Configure linting and formatting tools

### Phase 2: Foundational (Blocking Prerequisites)
Purpose: Core infrastructure that MUST be complete before ANY user story

⚠️ **CRITICAL**: No user story work can begin until this phase is complete

Example tasks:
- T004: Setup database schema and migrations framework
- T005 [P]: Implement authentication/authorization framework
- T006 [P]: Setup API routing and middleware structure
- T007: Create base models/entities
- T008: Configure error handling and logging
- T009: Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can begin

### Phase 3+: User Stories (Priority Order)
Each phase implements one user story independently

#### User Story 1 (Priority: P1) - MVP
**Goal**: Brief description
**Independent Test**: How to verify

- T010 [P] [US1]: Contract test for endpoint
- T011 [P] [US1]: Integration test for user journey
- T012 [P] [US1]: Create Entity1 model
- T013 [P] [US1]: Create Entity2 model
- T014 [US1]: Implement Service (depends on T012, T013)
- T015 [US1]: Implement endpoint/feature
- T016 [US1]: Add validation and error handling
- T017 [US1]: Add logging

**Checkpoint**: User Story 1 fully functional and independently testable

#### User Story 2 (Priority: P2)
Similar structure to US1, independently testable

#### User Story 3 (Priority: P3)
Similar structure to US1, independently testable

### Phase N: Polish & Cross-Cutting Concerns
- TXXX [P]: Documentation updates
- TXXX: Code cleanup and refactoring
- TXXX: Performance optimization
- TXXX [P]: Additional unit tests
- TXXX: Security hardening

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational completion
- **Polish (Final)**: Depends on all desired user stories complete

### User Story Dependencies
- All user stories depend on Foundational phase
- User stories can proceed in parallel (if team capacity allows)
- Or sequentially in priority order (P1 → P2 → P3)

### Within Each User Story
- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration

## Parallel Opportunities

### Setup Phase
All tasks marked [P] can run in parallel

### User Story Implementation
```bash
# Example: Launch all models together
Task: "Create Task model in src/models/task.py"
Task: "Create User model in src/models/user.py"

# Example: Launch all tests together
Task: "Contract test for POST /tasks"
Task: "Integration test for create task flow"
```

### Different User Stories
With multiple developers, different stories can proceed in parallel

## Implementation Strategies

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**
5. Deploy/demo if ready

### Incremental Delivery
1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy (MVP!)
3. Add User Story 2 → Test independently → Deploy
4. Add User Story 3 → Test independently → Deploy

### Parallel Team Strategy
1. Team completes Setup + Foundational together
2. Once Foundational done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`

## Example Usage

### Generate Tasks for Feature
```
/sp.tasks task-crud
```
Generates tasks for basic task CRUD operations.

### Generate Tasks for Complex Feature
```
/sp.tasks chatbot
```
Generates tasks for AI chatbot with MCP tools and database models.

## Constitution Compliance

### Spec-Driven Development
✅ Tasks based on user stories from spec
✅ Each task traceable to acceptance criteria
✅ No implementation without spec

### AI as Implementation Engine
✅ Tasks are implementation instructions for Claude Code
✅ Claude invokes with spec reference
✅ No manual code writing

### Human as System Architect
✅ Humans define user story priorities
✅ Humans validate task breakdown
✅ Humans approve before implementation

## Validation Checklist
Before tasks complete:
- [ ] Setup phase defined
- [ ] Foundational phase blocks user stories correctly
- [ ] Each user story organized independently
- [ ] Parallel opportunities marked [P]
- [ ] Dependencies clearly documented
- [ ] File paths included in descriptions
- [ ] Checkpoints defined

## Templates Used
- `specs/<feature-name>/tasks.md` follows `.specify/templates/tasks-template.md`

## See Also
- `/sp.spec` - Create feature specification
- `/sp.plan` - Create implementation plan
- `/sp.constitution` - View governing principles
