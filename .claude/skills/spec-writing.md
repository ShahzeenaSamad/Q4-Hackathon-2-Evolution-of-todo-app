# Skill: Spec Writing

## Metadata

**Skill Name:** `spec-writing`

**Description:** Create clear, structured markdown specifications including goals, constraints, flows, and acceptance criteria. No code allowed.

**Version:** 1.0

**Author:** Claude Code

**Created:** January 17, 2026

---

## Purpose

This skill creates comprehensive, structured markdown specifications for software features following spec-driven development principles. It enforces the rule that NO CODE should be generated during specification creation.

---

## When to Use

Use this skill when:
- User asks to create specifications for a feature
- User asks to write specs for a component, API, database schema, or UI
- User requests documentation of requirements
- Following spec-driven development workflow

**DO NOT use this skill when:**
- User explicitly asks for implementation/code
- User wants to modify existing code
- User requests debugging or testing

---

## Core Principles

1. **Spec-First:** Always create specifications before implementation
2. **No Code:** Never generate code during spec creation
3. **Structured:** Follow the standard spec template
4. **Complete:** Include all sections: goals, constraints, flows, acceptance criteria
5. **Clear:** Use simple, unambiguous language
6. **Testable:** Every requirement must have testable acceptance criteria

---

## Specification Template

Every specification MUST include the following sections:

### 1. Overview
- Feature name and purpose
- Context and background
- Scope (in-scope and out-of-scope)
- Target users/stakeholders

### 2. Goals
- Primary objectives
- Success metrics
- Desired outcomes

### 3. Constraints
- Technical constraints (technology stack, performance, security)
- Business constraints (timeline, resources, budget)
- Design constraints (UI/UX requirements, accessibility)

### 4. User Stories
- As a [role], I can [action] so that [benefit]
- Minimum 3-5 user stories per feature

### 5. Functional Requirements
- Detailed feature descriptions
- Input/output specifications
- Business rules
- Edge cases

### 6. Acceptance Criteria
- Testable conditions for each requirement
- Definition of Done
- Success metrics

### 7. Flows/Diagrams
- User flow diagrams (text-based or ASCII)
- Sequence flows
- State transitions
- Error handling flows

### 8. Data Models
- Data structures (if applicable)
- API contracts (if applicable)
- Database schemas (if applicable)
- UI mockups (text-based)

### 9. Non-Functional Requirements
- Performance requirements
- Security requirements
- Scalability requirements
- Usability requirements

### 10. Dependencies
- Technical dependencies
- Team dependencies
- External dependencies

### 11. Risks & Mitigation
- Potential risks
- Mitigation strategies
- Contingency plans

---

## Output Format

Specifications should be written in **Markdown** format with:

- Clear section headers (##, ###)
- Bullet points for lists
- Tables for structured data
- Code blocks only for examples (never implementation)
- ASCII diagrams for flows (when needed)

---

## Rules

### MUST DO:
- ✅ Write in clear, simple language
- ✅ Include all required sections
- ✅ Make requirements testable
- ✅ Define success criteria
- ✅ Document constraints and assumptions
- ✅ Use structured markdown format

### MUST NOT DO:
- ❌ Generate ANY code (Python, JavaScript, SQL, etc.)
- ❌ Provide implementation details
- ❌ Write pseudocode
- ❌ Include framework-specific details unless specified

---

## Examples

### Good Specification Excerpt:

```markdown
## User Stories

1. **Create Task**
   - As a user, I can create a task with a title and optional description
   - So that I can track my to-do items

## Acceptance Criteria

### AC-1: Title Validation
- **Given:** User is on create task page
- **When:** User enters task title
- **Then:**
  - Title must be 1-200 characters
  - Title cannot be empty
  - Special characters are allowed
  - System shows character counter
```

### Bad Specification Excerpt:

```python
def create_task(title, description):
    if not title:
        raise Error("Title required")
    return Task(title=title)
```

**WHY BAD:** This is CODE, not specification!

---

## Quality Checklist

Before finalizing a spec, verify:

- [ ] All required sections are present
- [ ] User stories are clear and complete
- [ ] Acceptance criteria are testable
- [ ] Constraints are documented
- [ ] No code is included
- [ ] Language is unambiguous
- [ ] Success metrics are defined
- [ ] Edge cases are considered

---

## Related Skills

- `fastapi-backend-implementer` - Implement specs in FastAPI backend
- `frontend-nextjs-builder` - Implement specs in Next.js frontend
- `qa-testing-validator` - Validate implementation against specs

---

## Usage Instructions

When invoked, this skill will:

1. **Analyze Request:** Understand what needs to be specified
2. **Ask Clarifications:** Ask targeted questions if requirements are unclear (max 3 questions)
3. **Create Spec:** Write comprehensive specification following template
4. **Review:** Self-check against quality checklist
5. **Output:** Present specification for user review

---

## File Location

Specifications should be saved in:
- Feature specs: `specs/features/[feature-name].md`
- API specs: `specs/api/[api-name].md`
- Database specs: `specs/database/[schema-name].md`
- UI specs: `specs/ui/[component-name].md`

---

## Version History

- **v1.0** (2026-01-17): Initial skill definition

---

**Skill Status:** ✅ Active
**Phase:** Phase II - Full-Stack Web Application
