---
description: "Manage project constitution - the governing document for all development"
---

# Constitution Management Command

## Usage
```
/sp.constitution [options]
```

## Description
The constitution is the supreme governing document for this project. It defines:
- Core principles that MUST be followed
- Development standards and workflows
- AI governance rules
- Architecture constraints
- Phase-specific requirements

## Options

### View Constitution
```
/sp.constitution
```
Display the current constitution.

### Amend Constitution
```
/sp.constitution --amend "Change description"
```
Propose an amendment to the constitution. Requires:
- Rationale (why change is needed)
- Impact analysis (what breaks/improves)
- Migration plan (how to transition)

## Constitution Location
- **Primary**: `CONSTITUTION.md` (root directory)
- **Reference**: `.specify/memory/constitution.md`

## Key Principles Summary

### I. Spec-Driven Development (NON-NEGOTIABLE)
- NO implementation without approved spec
- Specs must be written BEFORE any code generation
- Claude Code MUST be invoked with spec references

### II. AI as Implementation Engine
- Claude Code is the ONLY implementation engine
- Manual code writing is PROHIBITED
- Humans write specs; AI writes code

### III. Human as System Architect
- Humans design systems, make trade-off decisions
- AI generates code from specifications
- Humans validate AI-generated implementations

### IV. Reusability of Intelligence
- Create Agent Skills for repeated operations
- Develop Subagents for complex workflows
- Build Cloud-Native Blueprints

### V. Stateless & Cloud-Native Design
- All services MUST be stateless (except Phase I)
- State stored externally (database, cache, message queue)
- Design for 12-factor app principles

### VI. Security by Design
- Security at every phase
- JWT-based authentication (Phase II+)
- User isolation enforced
- Secrets never committed to git

### VII. Observability & Scalability
- Structured JSON logs with correlation IDs
- Metrics tracking (Phase IV+)
- Distributed tracing (Phase V)
- Health checks on all services

## Phase Requirements
- **Phase I**: In-Memory Python Console App
- **Phase II**: Full-Stack Web Application (Next.js + FastAPI + Neon DB)
- **Phase III**: AI-Powered Todo Chatbot (OpenAI Agents SDK + MCP)
- **Phase IV**: Local Kubernetes Deployment (Minikube + Helm)
- **Phase V**: Advanced Cloud Deployment (Kafka + Dapr + Managed K8s)

## Compliance Checklist
Before any code commit, verify:
- [ ] Spec exists and is referenced
- [ ] Code aligns with spec acceptance criteria
- [ ] No manual code writing
- [ ] Stateless design (Phase II+)
- [ ] Security requirements met
- [ ] Observability present

## Version History
- 1.0.0 (2026-01-16): Initial constitution for Hackathon II

## See Also
- `/sp.spec` - Create feature specifications
- `/sp.plan` - Create implementation plans
- `/sp.tasks` - Generate task lists
- `/sp.adr` - Document architectural decisions
