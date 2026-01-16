---
description: "Document architectural decisions with Architecture Decision Records"
---

# Architecture Decision Record Command

## Usage
```
/sp.adr <decision-title>
```

## Description
Creates an Architecture Decision Record (ADR) to document significant architectural decisions, their rationale, and consequences.

## What Requires an ADR?

Create an ADR when a decision is:
1. **Significant**: Long-term consequences for the system
2. **Architectural**: Affects system design, structure, or behavior
3. **Cross-cutting**: Influences multiple parts of the system

### Examples Requiring ADRs:
- Choosing between frameworks (Next.js vs React vs Vue)
- Database selection (PostgreSQL vs MongoDB vs Neon)
- Authentication approach (JWT vs Sessions vs OAuth)
- MCP tool design patterns
- Kafka vs RabbitMQ for event streaming
- Dapr integration strategy
- Microservices vs monolith
- API design (REST vs GraphQL vs gRPC)

### Examples NOT Requiring ADRs:
- Variable naming conventions
- Code formatting (handled by linters)
- Minor refactorings
- Bug fixes
- Feature implementations (covered by specs)

## ADR Structure

### 1. Title
Short, descriptive title
Example: "003-use-mcp-tools-for-ai-agent-integration"

### 2. Status
- **Proposed**: Under consideration
- **Accepted**: Decision made, actively implemented
- **Deprecated**: No longer recommended, but still in use
- **Superseded**: Replaced by newer decision (link to new ADR)

### 3. Context
What is the issue we're facing?
- Why are we making this decision?
- What problem are we solving?
- What are the constraints?

### 4. Decision
What are we doing?
- Clear statement of the decision
- What option was chosen
- Brief description of the approach

### 5. Rationale
Why this option?
- Benefits of this approach
- How it addresses the context
- What principles guide this decision

### 6. Consequences
### Positive (Benefits)
- What advantages does this bring?
- What problems does it solve?
- What opportunities does it enable?

### Negative (Drawbacks)
- What disadvantages exist?
- What problems might this cause?
- What constraints does this impose?

### Risks
- What could go wrong?
- How do we mitigate these risks?
- What are the warning signs?

### 7. Alternatives Considered
Option A, Option B, Option C, etc.
For each alternative:
- Description
- Why rejected (or ranked lower)

### 8. Related Decisions
- Links to related ADRs
- Dependencies on previous decisions
- Implications for future decisions

### 9. References
- Links to relevant specs
- External documentation
- Research sources

## Example ADR

```markdown
# ADR-001: Use Neon PostgreSQL as Primary Database

## Status
Accepted

## Context
We need a database for the Todo application that:
- Supports multi-user data isolation
- Provides ACID transactions
- Scales horizontally
- Integrates with FastAPI via SQLModel
- Offers free tier for hackathon

## Decision
Use Neon Serverless PostgreSQL as the primary database.

## Rationale
- Neon offers serverless PostgreSQL with automatic scaling
- Free tier available for hackathon participation
- Excellent Python ecosystem support via SQLModel
- Built-in connection pooling and scaling
- Branching feature for development/testing

## Consequences

### Positive
- Zero database administration overhead
- Automatic scaling based on load
- Development database branches for feature testing
- Compatible with SQLModel ORM
- Serverless pricing model

### Negative
- Vendor lock-in to Neon platform
- Cold start latency on first connection
- Limited configuration options compared to self-hosted

### Risks
- Service outage if Neon has downtime
- Potential cost increase at scale
Mitigation: Export backups regularly, monitor usage

## Alternatives Considered

### Self-hosted PostgreSQL
- Rejected: Requires server management, no free hosting

### MongoDB
- Rejected: Less suitable for relational task data, SQLModel designed for SQL

### SQLite
- Rejected: Not suitable for multi-user web application

## Related Decisions
- ADR-002: Use SQLModel as ORM layer
- ADR-005: Implement JWT-based user authentication

## References
- Neon documentation: https://neon.tech/docs
- SQLModel docs: https://sqlmodel.tiangolo.com
- Phase II spec: specs/features/task-crud/spec.md
```

## Output Location
```
history/adr/
├── 001-use-neon-postgresql.md
├── 002-use-sqlmodel-orm.md
├── 003-implement-mcp-tools.md
└── ...
```

## Numbering Scheme
- Sequential numbers starting at 001
- Use hyphen-separated slugs in filenames
- Reference by number in other ADRs

## Constitution Compliance

### Human as System Architect
✅ Architectural decisions made by humans
✅ Decisions documented with rationale
✅ AI implements based on ADR guidance

### Spec-Driven Development
✅ ADRs inform spec creation
✅ Specs reference relevant ADRs
✅ Implementation follows ADR decisions

## Example Usage

### Create Simple ADR
```
/sp.adr Use Next.js for Frontend Framework
```
Creates ADR documenting Next.js selection.

### Create Complex ADR
```
/sp.adr Implement Event-Driven Architecture with Kafka
```
Creates comprehensive ADR for Kafka integration decision.

## When to Create ADRs

### During Spec Creation
If spec introduces significant architectural choices, create ADR first

### During Planning
If `/sp.plan` identifies multiple valid approaches, document decision

### During Implementation
If unexpected trade-offs emerge, document decision and rationale

## ADR Quality Checklist
Before considering ADR complete:
- [ ] Clear decision statement
- [ ] Context and problem well-defined
- [ ] Rationale explains "why"
- [ ] Both positive and negative consequences listed
- [ ] At least 2 alternatives considered
- [ ] Risks identified and mitigations documented
- [ ] Related ADRs linked
- [ ] References included

## Templates Used
- `history/adr/<number>-<title>.md` follows `.specify/templates/adr-template.md`

## See Also
- `/sp.spec` - Create feature specification
- `/sp.plan` - Create implementation plan
- `/sp.constitution` - View governing principles
