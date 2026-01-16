---
description: "Show project status and progress"
---

# Project Status Command

## Usage
```
/sp.status [phase]
```

## Description
Shows current project status, including phases, features, and overall progress.

## Options

### Overall Status
```
/sp.status
```
Shows status of all phases and features.

### Specific Phase
```
/sp.status phase2
```
Shows status for Phase II only.

## Output Sections

### Project Overview
- Project name and vision
- Current phase
- Overall completion percentage
- Total points earned

### Phase Status
For each phase (I-V):
- Phase name and description
- Status: Not Started | In Progress | Completed
- Features completed / total
- Points earned
- Due date (if applicable)

### Feature Breakdown
- Feature specifications created
- Implementation plans ready
- Tasks generated
- Code implemented
- Tests passing

### Constitution Compliance
- Spec-Driven Development: ✅/❌
- AI Implementation Engine: ✅/❌
- Stateless Design: ✅/❌ (Phase II+)
- Security: ✅/❌
- Observability: ✅/❌

## Example Output

```
# Hackathon II - Project Status

## Overview
- Project: The Evolution of Todo
- Current Phase: Phase II - Full-Stack Web Application
- Overall Progress: 40% (400/1000 points)
- Status: On Track

## Phase Breakdown

### Phase I: In-Memory Console App (100 pts)
Status: ✅ Completed
- Features: 1/1 implemented
- Points: 100/100
- Completed: Dec 7, 2025

### Phase II: Full-Stack Web Application (150 pts)
Status: 🔄 In Progress
- Features: 3/5 implemented
  - ✅ Task CRUD operations
  - ✅ User authentication
  - ✅ Database setup
  - ⏳ Task filtering/sorting
  - ⏳ Responsive UI
- Points: 90/150
- Due: Dec 14, 2025

### Phase III: AI Chatbot (200 pts)
Status: ⏳ Not Started
- Due: Dec 21, 2025

### Phase IV: Kubernetes Deployment (250 pts)
Status: ⏳ Not Started
- Due: Jan 4, 2026

### Phase V: Cloud Deployment (300 pts)
Status: ⏳ Not Started
- Due: Jan 18, 2026

## Constitution Compliance
- Spec-Driven Development: ✅ All features have specs
- AI Implementation Engine: ✅ No manual code
- Stateless Design: ✅ Database-backed state
- Security: ✅ JWT auth, user isolation
- Observability: ✅ Structured logging

## Next Steps
1. Complete task filtering feature
2. Implement responsive UI
3. Write integration tests
4. Deploy to Vercel for demo
```

## Phase Details

### Phase I: Console App
**Requirements:**
- Python 3.13+ with UV
- In-memory task storage
- 5 basic features
- Spec-driven development

**Deliverables:**
- ✅ `/phase1-console/src/` with Python code
- ✅ `/specs/features/task-crud/spec.md`
- ✅ Working console application

**Status Criteria:**
- All 5 features working
- Spec exists and is followed
- Clean code principles

### Phase II: Web Application
**Requirements:**
- Next.js 16+ frontend
- FastAPI backend
- Neon PostgreSQL database
- Better Auth with JWT
- RESTful API endpoints

**Deliverables:**
- ✅ `/phase2-web/frontend/` Next.js app
- ✅ `/phase2-web/backend/` FastAPI app
- ✅ `/specs/features/` specifications
- ✅ `/specs/api/rest-endpoints.md`
- ✅ `/specs/database/schema.md`

**Status Criteria:**
- All API endpoints working
- User authentication functional
- Database persistence verified
- Frontend-backend integration complete

### Phase III: AI Chatbot
**Requirements:**
- OpenAI ChatKit UI
- FastAPI + OpenAI Agents SDK
- Official MCP SDK
- Stateless chat endpoint
- Database-backed conversations

**Deliverables:**
- ⏳ MCP tools for task operations
- ⏳ Chat endpoint with agent
- ⏳ Conversation/message models
- ⏳ Natural language interface

**Status Criteria:**
- Chatbot understands commands
- MCP tools functional
- Conversations persist across sessions
- Stateless design verified

### Phase IV: Kubernetes Deployment
**Requirements:**
- Docker containerization
- Minikube local deployment
- Helm charts
- kubectl-ai/kagent usage

**Deliverables:**
- ⏳ Dockerfiles for frontend/backend
- ⏳ Helm charts
- ⏳ K8s manifests
- ⏳ Deployment blueprint

**Status Criteria:**
- Containers build and run
- Deploys to Minikube successfully
- Helm charts tested
- Blueprint created

### Phase V: Cloud Deployment
**Requirements:**
- DigitalOcean/GCP/Azure K8s
- Kafka (Redpanda Cloud)
- Dapr integration
- CI/CD pipeline
- Advanced features

**Deliverables:**
- ⏳ Dapr components
- ⏳ Kafka configurations
- ⏳ GitHub Actions workflows
- ⏳ Cloud deployment blueprint

**Status Criteria:**
- Deploys to managed K8s
- Kafka event streaming works
- Dapr building blocks functional
- CI/CD pipeline active

## Quick Checks

### Spec Compliance
```bash
# Check all features have specs
find specs/features -name "spec.md" | wc -l

# Check specs referenced in code
grep -r "@specs/" phase2-web/
```

### Code Quality
```bash
# Check for manual code (should be minimal)
git log --author="Your Name" --oneline | wc -l

# Check AI-generated code
git log --author="Claude" --oneline | wc -l
```

### Constitution Checks
```bash
# Stateless design (Phase II+)
grep -r "state" phase2-web/backend/src/ | grep -i "cache\|session"

# Security - user isolation
grep -r "user_id" phase2-web/backend/src/ | wc -l

# Observability
grep -r "logger\|log" phase2-web/backend/src/ | wc -l
```

## Bonus Points Tracking

### Reusable Intelligence (+200)
- ✅ Agent Skills created: 5
- ⏳ Subagents developed: 0
- ⏳ Blueprints created: 0

### Cloud-Native Blueprints (+200)
- ⏳ Deployment blueprints: 0

### Multi-language Support (+100)
- ⏳ Urdu in chatbot: No

### Voice Commands (+200)
- ⏳ Voice input: No

**Total Bonus Points:** 0/600

## Next Actions

Based on current status, suggested next actions:

### If Phase II In Progress
1. Complete remaining features
2. Write integration tests
3. Deploy to Vercel
4. Create demo video

### If Phase II Complete
1. Review Phase III requirements
2. Create chatbot specification
3. Set up OpenAI ChatKit
4. Design MCP tools

### If Behind Schedule
1. Focus on MVP features first
2. Defer non-critical items
3. Consider simplifying scope
4. Request extension if needed

## Related Commands
- `/sp.spec` - Create missing specs
- `/sp.plan` - Create implementation plans
- `/sp.tasks` - Generate task lists
- `/sp.constitution` - Review governance

## Related Agents
- @.claude/agents/task-manager - Track progress
- @.claude/agents/feature-developer - Implement features
