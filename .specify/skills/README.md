# Reusable Skills Library

This directory contains reusable skills for the Evolution of Todo project. Skills are self-contained, documented capabilities that can be applied across multiple phases.

## Available Skills

### 1. Database Session Management
**File:** `database-session.skill.md`

**Capabilities:**
- Get database sessions with proper error handling
- Execute operations in transactions with automatic rollback
- Query with pagination support

**When to Use:**
- Any database operation requiring a session
- Batch operations or transactions
- Testing with database fixtures

**Dependencies:**
- SQLModel Session from `db.py`

---

### 2. MCP Tool Invocation
**File:** `mcp-tool-invocation.skill.md`

**Capabilities:**
- Invoke MCP tools with error handling
- Chain multiple tools in sequence
- Parse tool responses and handle errors

**When to Use:**
- Agent needs to interact with database through MCP tools
- Executing task operations (add/list/complete/update/delete)
- Testing MCP tool functionality

**Dependencies:**
- mcp_tools package from `phase-3-chatbot/backend`

---

### 3. Conversation Management
**File:** `conversation-management.skill.md`

**Capabilities:**
- Create and manage conversations
- Add messages with role tracking (user/assistant)
- Build conversation history for agent context
- Limit history size for token management

**When to Use:**
- Chatbot needs to maintain conversation history
- Agent requires context from previous messages
- Testing conversation flows

**Dependencies:**
- ConversationService from `services/conversation_svc.py`
- HistoryBuilder from `services/history_builder.py`

---

### 4. Agent Intent Detection
**File:** `agent-intent-detection.skill.md`

**Capabilities:**
- Keyword-based intent detection (fast, no API)
- AI-based intent detection using GPT-4o (accurate)
- Entity extraction from messages
- Intent-to-tool routing

**When to Use:**
- Agent needs to understand what user wants to do
- Routing user messages to appropriate MCP tools
- Building conversational agents

**Dependencies:**
- OpenAI client (for AI-based detection)
- Regular expressions (for entity extraction)

---

### 5. Error Handling & Recovery
**File:** `error-handling-recovery.skill.md`

**Capabilities:**
- Handle validation, not found, and ownership errors
- Database error handling with user-friendly messages
- API error handling (OpenAI rate limits, quotas)
- Retry logic with exponential backoff
- Graceful degradation and fallback strategies

**When to Use:**
- Any MCP tool invocation
- Agent response generation
- Database operations
- API calls to external services

**Dependencies:**
- Custom exceptions from `mcp_tools/exceptions.py`
- Logging module

---

### 6. Dockerfile Generation
**File:** `dockerfile-generation.skill.md`

**Capabilities:**
- Generate optimized Dockerfiles for Next.js frontend
- Generate production-ready Dockerfiles for FastAPI backend
- Multi-stage builds with layer caching
- Docker Compose configuration for local development
- Security best practices (non-root users, health checks)

**When to Use:**
- Containerizing applications for Kubernetes deployment
- Creating production-ready container images
- Implementing Docker optimization strategies
- Setting up local development environments

**Dependencies:**
- Docker 20.10+ or Docker Desktop 4.53+
- Next.js 16+ for frontend
- Python 3.13+ for backend

---

### 7. Docker Image Building
**File:** `image-building.skill.md`

**Capabilities:**
- Build Docker images with optimization strategies
- Multi-architecture image builds (AMD64, ARM64)
- Image tagging and version management
- Push to container registries (Docker Hub, GHCR, ACR)
- CI/CD integration for automated builds

**When to Use:**
- Building and managing Docker images
- Implementing image build pipelines
- Managing image versions and tags
- Optimizing image sizes and build times

**Dependencies:**
- Docker 20.10+ with BuildKit
- Container registry access
- CI/CD platform (optional)

---

### 8. Kubernetes Deployment
**File:** `k8s-deployment.skill.md`

**Capabilities:**
- Create Kubernetes Deployments, Services, ConfigMaps, Secrets
- Deploy applications to Minikube (local) and cloud (DOKS, GKE, AKS)
- Implement health checks and probes
- Configure resource limits and requests
- Rolling updates and rollbacks

**When to Use:**
- Deploying containerized applications to Kubernetes
- Managing application lifecycle in Kubernetes
- Configuring environment-specific deployments
- Implementing rolling update strategies

**Dependencies:**
- Kubernetes cluster (Minikube, DOKS, GKE, AKS)
- kubectl CLI tool
- Container images in registry

---

### 9. Kubernetes Scaling
**File:** `k8s-scaling.skill.md`

**Capabilities:**
- Horizontal Pod Autoscaler (HPA) based on CPU/memory
- Vertical Pod Autoscaler (VPA) for resource optimization
- Manual scaling operations
- Scaling behavior configuration
- Cluster autoscaler for cloud providers

**When to Use:**
- Applications need to handle increased traffic/load
- Implementing auto-scaling based on metrics
- Optimizing resource allocation
- Cost-effective scaling strategies

**Dependencies:**
- Kubernetes cluster with Metrics Server
- Deployments with resource requests configured
- Sufficient cluster capacity

---

### 10. Helm Chart Generation
**File:** `helm-chart-generation.skill.md`

**Capabilities:**
- Create Helm charts for applications
- Package applications for deployment
- Manage environment-specific configurations (dev, staging, prod)
- Template Kubernetes resources
- Deploy and manage releases

**When to Use:**
- Packaging applications for deployment
- Managing environment-specific configurations
- Simplifying complex Kubernetes deployments
- Versioning application releases

**Dependencies:**
- Helm 3.x CLI tool
- Kubernetes cluster access
- Application container images

---

### 11. Cluster Health Analysis
**File:** `cluster-health-analysis.skill.md`

**Capabilities:**
- Monitor cluster health and performance
- Check node status, pod health, resource utilization
- Analyze logs and troubleshoot issues
- Use kubectl-ai for intelligent analysis
- Set up health check scripts and alerts

**When to Use:**
- Monitoring cluster health and performance
- Troubleshooting application issues
- Analyzing resource utilization patterns
- Investigating pod failures and crashes

**Dependencies:**
- kubectl CLI tool
- metrics-server installed on cluster
- kubectl-ai plugin (optional)
- OpenAI API key (for kubectl-ai)

---

### 12. Specification Parsing
**File:** `spec-parsing.skill.md`

**Capabilities:**
- Parse high-level application specifications
- Convert specs to Kubernetes manifests and Helm charts
- Validate deployments against specifications
- Generate infrastructure from spec documents
- CI/CD integration for spec-driven deployment

**When to Use:**
- Converting feature specifications into deployment artifacts
- Translating architectural requirements into Kubernetes resources
- Generating infrastructure from specification documents
- Implementing spec-driven DevOps workflows

**Dependencies:**
- Python 3.11+
- PyYAML library
- Kubernetes Python client
- Specification documents (YAML/JSON)

---

## How to Use Skills

### 1. Import Relevant Skill Functions
```python
# From Database Session Management skill
from skills.database_session import get_db_session, execute_in_transaction

# From MCP Tool Invocation skill
from skills.mcp_tool_invocation import invoke_tool, get_tool

# From Conversation Management skill
from skills.conversation_management import (
    create_conversation,
    add_message,
    get_conversation_history
)
```

### 2. Apply Skill Patterns
```python
# Using Database Session skill
with SessionLocal() as session:
    result = execute_in_transaction(
        session,
        lambda s: s.execute(select(Task).where(Task.user_id == user_id))
    )

# Using MCP Tool Invocation skill
result = invoke_tool(
    "add_task",
    session,
    user_id="user-123",
    title="Buy milk"
)
```

### 3. Combine Skills
```python
def handle_user_message(user_id: str, message: str):
    # Database Session skill
    db = SessionLocal()

    try:
        # Conversation Management skill
        conv_id = create_conversation(user_id, db)
        add_message(conv_id, "user", message, db)

        # Intent Detection skill
        intent = detect_intent_keywords(message)

        # MCP Tool Invocation skill
        result = invoke_tool(intent["intent"], db, user_id=user_id)

        # Error Handling skill
        if not result["success"]:
            return format_error_response(result["error"])

        add_message(conv_id, "assistant", result["data"]["response"], db)
        return result["data"]

    finally:
        db.close()
```

## Skill Design Principles

1. **Self-Contained:** Each skill includes all necessary code examples
2. **Reusable:** Skills apply across multiple phases and use cases
3. **Documented:** Clear descriptions of when and how to use
4. **Testable:** Includes testing patterns for validation
5. **Composable:** Skills can be combined for complex operations

## Adding New Skills

When creating a new skill:

1. **Choose a clear name:** Describe the capability (e.g., "user-authentication")
2. **Define scope:** What specific problem does it solve?
3. **Document usage:** When to use, with examples
4. **List dependencies:** What packages/modules are required?
5. **Provide patterns:** Common usage patterns and best practices
6. **Include tests:** How to validate the skill works correctly

## Skill Template

```markdown
# [Skill Name]

## Description
[Brief description of what this skill does]

## When to Use
- [Use case 1]
- [Use case 2]

## Capabilities
### [Capability 1]
[Code example]

### [Capability 2]
[Code example]

## Error Handling
[Common errors and how to handle them]

## Best Practices
1. [Best practice 1]
2. [Best practice 2]

## Dependencies
- [Dependency 1]
- [Dependency 2]
```

## Contributing

When you identify a reusable pattern across phases:
1. Extract it into a skill
2. Document it with examples
3. Add it to this README
4. Update related phases to use the skill

## Version History

- **v2.0** (2026-01-29): Phase IV Kubernetes skills added
  - Dockerfile Generation
  - Docker Image Building
  - Kubernetes Deployment
  - Kubernetes Scaling
  - Helm Chart Generation
  - Cluster Health Analysis
  - Specification Parsing

- **v1.0** (2025-01-22): Initial 5 skills created
  - Database Session Management
  - MCP Tool Invocation
  - Conversation Management
  - Agent Intent Detection
  - Error Handling & Recovery

## Phase Skills Mapping

### Phase I-III: Core Application Skills
1. Database Session Management
2. MCP Tool Invocation
3. Conversation Management
4. Agent Intent Detection
5. Error Handling & Recovery

### Phase IV: Kubernetes Deployment Skills
6. Dockerfile Generation
7. Docker Image Building
8. Kubernetes Deployment
9. Kubernetes Scaling
10. Helm Chart Generation
11. Cluster Health Analysis
12. Specification Parsing

## Quick Reference

### For Phase IV Development:
```bash
# 1. Containerize application
-> dockerfile-generation.skill.md
-> image-building.skill.md

# 2. Deploy to Kubernetes
-> k8s-deployment.skill.md
-> helm-chart-generation.skill.md

# 3. Configure scaling
-> k8s-scaling.skill.md

# 4. Monitor and troubleshoot
-> cluster-health-analysis.skill.md

# 5. Automate from specs
-> spec-parsing.skill.md
```

### Skills by Category:

**Container & Image Management:**
- Dockerfile Generation (#6)
- Docker Image Building (#7)

**Kubernetes Operations:**
- Kubernetes Deployment (#8)
- Kubernetes Scaling (#9)
- Helm Chart Generation (#10)
- Cluster Health Analysis (#11)

**Automation:**
- Specification Parsing (#12)

**Application Logic (Phases I-III):**
- Database Session Management (#1)
- MCP Tool Invocation (#2)
- Conversation Management (#3)
- Agent Intent Detection (#4)
- Error Handling & Recovery (#5)
