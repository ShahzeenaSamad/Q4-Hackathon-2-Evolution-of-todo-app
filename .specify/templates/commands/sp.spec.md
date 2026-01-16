---
description: "Create a feature specification following Spec-Driven Development principles"
---

# Feature Specification Command

## Usage
```
/sp.spec <feature-name> [description]
```

## Description
Creates a comprehensive feature specification that serves as the authoritative source of truth for implementation.

## Spec Structure

### 1. User Scenarios & Testing (MANDATORY)
- User stories with priorities (P1, P2, P3)
- Acceptance scenarios (Given/When/Then format)
- Independent testability for each story
- Edge cases and error paths

### 2. Requirements (MANDATORY)
- Functional requirements (FR-001, FR-002, etc.)
- Key entities and relationships
- Clear, measurable acceptance criteria

### 3. Success Criteria (MANDATORY)
- Measurable outcomes
- Performance budgets
- User satisfaction metrics
- Business metrics

## Output Files
```
specs/<feature-name>/
├── spec.md              # Main specification (this command)
├── plan.md              # Implementation plan (/sp.plan)
└── tasks.md             # Task list (/sp.tasks)
```

## User Story Format

### User Story 1 - [Title] (Priority: P1)
**Description**: [User journey in plain language]

**Why this priority**: [Value and priority justification]

**Independent Test**: [How to test independently]

**Acceptance Scenarios**:
1. Given [initial state], When [action], Then [expected outcome]
2. Given [initial state], When [action], Then [expected outcome]

## Example Usage

### Create Basic Feature Spec
```
/sp.spec task-crud
```
Creates specification for task CRUD operations.

### Create with Description
```
/sp.spec authentication "User signup and login with JWT"
```
Creates authentication feature with description.

### Complex Feature
```
/sp.spec chatbot "AI-powered todo management with natural language"
```
Creates comprehensive chatbot specification.

## Constitution Compliance

### Spec-Driven Development Principle
✅ Spec MUST be written BEFORE any implementation
✅ Claude Code MUST be invoked with spec reference
✅ If output incorrect, refine spec—don't fix code manually

### AI as Implementation Engine
✅ Humans write specs
✅ AI writes code from spec
✅ No manual code writing

## Post-Spec Workflow

1. **Review Spec**
   - Verify all user stories have priorities
   - Check acceptance criteria are testable
   - Ensure requirements are clear

2. **Create Plan** (`/sp.plan <feature-name>`)
   - Research technical approach
   - Define data models
   - Design API contracts

3. **Generate Tasks** (`/sp.tasks <feature-name>`)
   - Break down into implementable tasks
   - Organize by user story
   - Mark parallel opportunities

4. **Implement via Claude Code**
   ```
   "@specs/features/<feature-name>/spec.md implement [feature]"
   ```

5. **Validate**
   - Run tests if defined
   - Verify acceptance criteria
   - Document deviations

## Validation Checklist
Before considering spec complete:
- [ ] At least 1 user story defined
- [ ] All stories have priorities (P1, P2, P3)
- [ ] Acceptance scenarios use Given/When/Then
- [ ] Functional requirements numbered (FR-001, FR-002, etc.)
- [ ] Success criteria are measurable
- [ ] Edge cases documented
- [ ] Error paths defined

## Templates Used
- `/specs/features/<feature-name>/spec.md` follows `.specify/templates/spec-template.md`

## See Also
- `/sp.plan` - Create implementation plan
- `/sp.tasks` - Generate task breakdown
- `/sp.constitution` - View governing principles
- `/sp.adr` - Document architectural decisions
