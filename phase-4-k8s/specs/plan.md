# Implementation Plan: Local Kubernetes Deployment for Todo AI Chatbot

**Feature Branch**: `phase-4-k8s`
**Created**: 2026-01-30
**Status**: Draft
**Based on**: [spec.md](./spec.md)

## Summary

This plan implements a local Kubernetes deployment for the Phase III Todo AI Chatbot using Docker, Minikube, Helm charts, and AI-powered DevOps agents (kubectl-ai, kagent). The system enables developers to deploy and manage a production-like containerized chatbot entirely on local hardware with zero cloud costs, demonstrating spec-driven infrastructure automation and AI-augmented DevOps workflows.

**Technical Approach**:
1. **Containerization**: Multi-stage Docker builds for Next.js frontend and FastAPI backend with minimal base images (alpine/distroless)
2. **Kubernetes Deployment**: Minikube cluster with Deployments, Services, ConfigMaps, Secrets, and HPA
3. **Package Management**: Helm charts for templating, environment-specific values, and release management
4. **AI DevOps**: kubectl-ai for deployment operations (primary method), kagent for cluster health analysis, Docker AI for image optimization
5. **Service Exposure**: Minikube tunnel provides stable LoadBalancer IP for local browser access

## Technical Context

### Technology Stack

**Frontend**:
- Framework: Next.js 16+ (App Router architecture)
- UI: Tailwind CSS with neon cyan theme
- Runtime: Node.js 20+ alpine-based container
- Port: 3000 (internal)

**Backend**:
- Framework: FastAPI (Python 3.13+)
- Database: Neon PostgreSQL (external managed service)
- AI: OpenAI API for chatbot functionality
- Runtime: Python 3.13+ slim/alpine-based container
- Port: 8000 (internal)

**Container Runtime**:
- Platform: Docker Desktop 4.53+
- Build strategy: Multi-stage builds for optimization
- Base images: node:20-alpine (frontend), python:3.13-slim (backend)
- Security: Non-root user, read-only root filesystem, health checks

**Orchestration**:
- Distribution: Minikube 1.32+ (local single-node cluster)
- Runtime: Docker container driver (via Docker Desktop)
- Resources: 8GB RAM, 4 CPU cores minimum
- Add-ons: dashboard, metrics-server, tunnel

**Package Management**:
- Helm 3.16+ for templating and release management
- Chart structure: Single umbrella chart with frontend and backend components
- Values files: values.yaml (default), values-dev.yaml, values-prod.yaml

**AI DevOps Tools**:
- kubectl-ai: Generate Kubernetes manifests from natural language (primary deployment method)
- kagent: Analyze cluster health, resource utilization, optimization opportunities
- Docker AI (Gordon): Optimize Dockerfile and image builds
- Fallback: Manual kubectl, Helm, Docker commands when AI fails

### Dependencies

**External Services**:
- Neon Database: PostgreSQL database (existing from Phase III)
- OpenAI API: Chatbot AI responses (existing from Phase III)

**Development Tools**:
- Docker Desktop: Container runtime
- Minikube: Local Kubernetes cluster
- kubectl 1.32+: Kubernetes CLI
- Helm 3.16+: Package manager
- kubectl-ai: AI Kubernetes assistant (requires OpenAI API access)
- kagent: AI cluster analyzer (requires OpenAI API access)

**Phase III Artifacts**:
- Frontend: Next.js 16+ application in `phase-3-chatbot/frontend/`
- Backend: FastAPI application in `phase-3-chatbot/backend/`
- Configuration: Environment variables, API endpoints

### Platforms

**Development**:
- OS: Windows 10/11, macOS, Linux
- Architecture: x64 or ARM64 (Apple Silicon)
- Network: Local machine, localhost access via Minikube tunnel

**Deployment Target**:
- Environment: Local Minikube cluster only
- Namespaces: todo-chatbot-dev, todo-chatbot-prod
- Services: LoadBalancer (via Minikube tunnel) for frontend, ClusterIP for backend

### Performance Goals

**Build Time**:
- Frontend image build: Under 3 minutes
- Backend image build: Under 5 minutes
- Total build time: Under 8 minutes

**Deployment Time**:
- Helm install: Under 3 minutes
- Pod startup: Under 30 seconds
- Rolling update: Under 2 minutes
- End-to-end deployment: Under 10 minutes

**Runtime Performance**:
- Application response time: Under 500ms (p95)
- Pod resource limits: CPU <70%, Memory <80% under normal load
- Health check interval: 10 seconds
- Health check timeout: 5 seconds

**Image Size**:
- Frontend compressed: Under 100MB
- Backend compressed: Under 200MB

### Constraints & Invariants

**Constraints**:
1. **Local Only**: No cloud-based deployments (EKS, GKE, AKS)
2. **Minikube Only**: No other Kubernetes distributions
3. **Helm Only**: No kubectl apply only, no Docker Compose
4. **Docker Desktop Required**: No containerd, CRI-O
5. **phase-4-k8s/ Folder**: All Phase IV work must be in phase-4-k8s/ directory
6. **AI-First**: kubectl-ai/kagent are primary methods with manual fallback

**Invariants**:
1. **Spec-Driven**: All Kubernetes manifests derived from specification, not manual YAML
2. **Security**: Containers run as non-root, read-only root filesystem
3. **Reproducibility**: Deployment works identically from specification alone
4. **Observability**: All pods have health checks, logs accessible via kubectl
5. **Rolling Updates**: Zero-downtime deployments with RollingUpdate strategy

### Non-Goals

**Out of Scope**:
- Cloud-based Kubernetes deployments (EKS, GKE, AKS, DOKS)
- Production-grade CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- Advanced security hardening (RBAC, pod security policies, network policies)
- Secrets management tools (Vault, external secret stores)
- Full monitoring stack (Prometheus, Grafana, Jaeger, ELK)
- Service mesh (Istio, Linkerd)
- Multi-cluster deployment
- Disaster recovery procedures
- Backup and restore strategies
- Production SLAs or SLOs (local development environment only)

## Constitution Check

### Principle 10: Spec-Driven Infrastructure Automation

**Gate**: Are all Kubernetes manifests generated from specifications?

**Status**: ✅ PASS

**Evidence**:
- Specification (spec.md) defines all infrastructure requirements (48 functional requirements)
- Helm charts provide templating engine to generate manifests from specification
- No manual Kubernetes YAML in implementation
- All deployment configuration derived from Helm values files

**Compliance**:
- FR-008 to FR-015: Kubernetes Deployment requirements specified
- FR-016 to FR-023: Helm Chart requirements specified
- FR-033: Deployment reproducible from specifications alone
- Constitution Section: "All Kubernetes manifests MUST be generated from specs, not manual YAML"

---

### Principle 11: AI-Augmented DevOps

**Gate**: Are AI agents the primary method for deployment operations?

**Status**: ✅ PASS

**Evidence**:
- FR-029: AI agents MUST be PRIMARY method for deployment operations
- FR-024 to FR-028: Specific kubectl-ai and kagent usage requirements
- FR-030: Manual fallback provided when AI fails
- Clarification Q2: "AI agents are primary method with manual fallback"

**Compliance**:
- Primary: kubectl-ai for deploy/scale/debug operations
- Primary: kagent for cluster health analysis
- Primary: Docker AI for Dockerfile optimization
- Fallback: Manual kubectl, Helm, Docker commands
- Constitution Section: "Prefer AI agents over manual CLI usage wherever possible"

---

### Principle 12: Cloud-Native Best Practices

**Gate**: Does deployment follow Kubernetes-native patterns?

**Status**: ✅ PASS

**Evidence**:
- FR-011: Minimum 2 replicas for high availability
- FR-012: Resource requests and limits configured
- FR-013: Liveness and readiness probes defined
- FR-014: RollingUpdate strategy for zero-downtime updates
- FR-015: Security context (non-root, read-only root filesystem)
- FR-037: HPA enabled for auto-scaling (2-10 replica range)

**Compliance**:
- Stateless services (frontend, backend)
- Horizontal scaling via HPA
- Declarative configuration (Helm charts)
- Health probes for self-healing
- Resource quotas for stability

---

### Principle 13: Local Reproducibility

**Gate**: Is deployment fully local and reproducible?

**Status**: ✅ PASS

**Evidence**:
- FR-031: Deployment MUST work entirely on local Minikube
- FR-032: Complete teardown and redeploy in under 10 minutes
- FR-033: Deployment reproducible from specifications alone
- FR-034: Accessible via Minikube tunnel (no cloud dependencies)
- Clarification Q4: Configuration split between Dockerfile (runtime) and Helm (environment)

**Compliance**:
- Zero cloud costs
- Identical deployment from spec
- <10 minute deployment cycle
- All dependencies: Docker Desktop, Minikube, Helm (local tools)

---

### Principle 14: Infrastructure Observability

**Gate**: Is deployment observable and debuggable?

**Status**: ✅ PASS

**Evidence**:
- FR-038 to FR-043: Observability requirements (6 requirements)
- FR-038: Pod logs accessible via kubectl
- FR-039: Metrics endpoints for monitoring
- FR-040: Pod status and health checks via kubectl
- FR-041: kubectl top commands for resource usage
- FR-042: Health checks validate both frontend and backend
- FR-043: Clear error messages and troubleshooting guidance

**Compliance**:
- kubectl logs for all pods
- kubectl top for resource monitoring
- kubectl describe for pod status
- Minikube dashboard for visualization
- kagent insights for optimization

---

## Project Structure

```
phase-4-k8s/
├── specs/
│   ├── spec.md              # Feature specification
│   ├── plan.md              # This implementation plan
│   ├── research.md          # Phase 0 research findings
│   ├── data-model.md        # Phase 1 data model
│   ├── contracts/           # Phase 1 service contracts
│   │   ├── frontend-api.md  # Frontend service contract
│   │   ├── backend-api.md   # Backend service contract
│   │   └── health-checks.md # Health check contracts
│   └── quickstart.md        # Quick start guide
├── docker/
│   ├── frontend/
│   │   ├── Dockerfile       # Next.js frontend multi-stage build
│   │   └── .dockerignore    # Build optimizations
│   └── backend/
│       ├── Dockerfile       # FastAPI backend multi-stage build
│       └── .dockerignore    # Build optimizations
├── helm/
│   ├── Chart.yaml           # Helm chart metadata
│   ├── values.yaml          # Default configuration (local dev)
│   ├── values-dev.yaml      # Development environment overrides
│   ├── values-prod.yaml     # Production-like environment overrides
│   └── templates/
│       ├── _helpers.tpl     # Template helpers
│       ├── frontend/
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   ├── hpa.yaml
│       │   └── configmap.yaml
│       └── backend/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── hpa.yaml
│           ├── configmap.yaml
│           └── secret.yaml
├── k8s/
│   ├── manifests/           # Generated Kubernetes manifests (for reference)
│   └── overlays/            # Environment-specific overlays (if needed)
└── scripts/
    ├── build-images.sh      # Build Docker images
    ├── deploy.sh            # Deploy via Helm
    ├── teardown.sh          # Teardown deployment
    └── test-deployment.sh   # Smoke tests
```

## Phase 0: Research & Decisions

### Decision 1: Container Runtime Choice

**Question**: Which container runtime to use for local Kubernetes?

**Decision**: Docker Desktop

**Rationale**:
- Native integration with Minikube (Docker driver)
- Widely adopted for local development
- Best tool support for desktop development
- Simplified workflow (no separate container runtime setup)

**Alternatives Considered**:
- containerd: More production-like, but harder to debug locally
- CRI-O: Lightweight, but not supported on Minikube Windows
- Podman: Rootless design, but Minikube integration is experimental

**References**: [Minikube Docker Driver](https://minikube.sigs.k8s.io/docs/drivers/docker/)

---

### Decision 2: Kubernetes Distribution

**Question**: Which Kubernetes distribution for local deployment?

**Decision**: Minikube

**Rationale**:
- Single-node cluster ideal for local development
- Cross-platform support (Windows, macOS, Linux)
- Easy setup and teardown
- Built-in LoadBalancer support via tunnel
- Low resource footprint compared to kind/k3d

**Alternatives Considered**:
- kind (Kubernetes in Docker): Faster startup, but no built-in tunnel
- k3d: Lightweight, but LoadBalancer requires extra setup
- MicroK8s: Production-like, but complex for local dev
- Docker Desktop Kubernetes: Too opinionated, harder to reset

**References**: [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

---

### Decision 3: Service Exposure Strategy

**Question**: How to expose frontend service to local browser?

**Decision**: Minikube Tunnel (LoadBalancer IP)

**Rationale**:
- Provides stable LoadBalancer IP (typically 127.0.0.1)
- Works consistently across operating systems
- Most developer-friendly experience
- No ingress controller setup complexity
- Direct URL access (http://127.0.0.1:3000)

**Alternatives Considered**:
- NodePort: Requires dynamic port tracking, less developer-friendly
- Ingress: More production-like, but adds complexity for local dev
- Port-forwarding: Works for single pod, not LoadBalancer services

**References**: [Minikube Tunnel](https://minikube.sigs.k8s.io/docs/commands/tunnel/)

---

### Decision 4: Configuration Management Approach

**Question**: How to split configuration between Docker and Helm?

**Decision**: Dockerfiles define runtime (ports, commands), Helm values override environment variables

**Rationale**:
- Follows Docker best practices (images are portable)
- Dockerfiles specify essential runtime (EXPOSE, CMD/ENTRYPOINT)
- Helm values provide environment-specific config (API endpoints, database URLs)
- Clear separation of concerns: runtime vs environment

**Alternatives Considered**:
- All config in Dockerfiles: Not portable across environments
- All config in Helm: Violates Docker best practices (images should know their ports)

**References**: [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

### Decision 5: AI Automation Level

**Question**: Should AI agents be primary method or demonstration-only?

**Decision**: AI agents are PRIMARY method with manual fallback

**Rationale**:
- Aligns with Phase IV constitution principle (AI-Augmented DevOps)
- Enables learning AI-assisted workflows
- Manual fallback ensures safety when AI fails
- Demonstrates practical AI-augmented DevOps

**Alternatives Considered**:
- Manual-only: No AI learning, violates constitution
- AI-only: Too risky, no safety net when AI fails

**References**: Constitution Principle 11 (AI-Augmented DevOps)

---

### Decision 6: Success Criteria Definition

**Question**: What defines a successful deployment?

**Decision**: All critical components healthy (pods Running + health checks pass + app accessible)

**Rationale**:
- Balanced approach: requires all three conditions
- Focuses on actual functionality, not just resource status
- Allows for some non-critical issues while ensuring system works
- Measurable: `kubectl get pods` shows Running, health checks pass, browser loads app

**Alternatives Considered**:
- Pods Running only: Too shallow, pods might be unhealthy
- All resources perfect: Too strict, minor issues shouldn't fail deployment

**References**: Spec SC-001, Clarification Q3

---

### Decision 7: Rollback and Teardown Behavior

**Question**: What happens during rollback and teardown?

**Decision**: Rollback restores previous deployment state, teardown removes all Kubernetes resources

**Rationale**:
- Follows standard Kubernetes behavior
- Helm rollback reverts to previous deployment (pod template, replica count, config)
- Teardown cleanly removes all resources (deployments, services, configmaps, secrets, PVs)
- No orphaned resources remain

**Alternatives Considered**:
- Custom rollback scripts: Non-standard, harder to maintain
- Partial teardown: Risk of orphaned resources consuming disk space

**References**: [Helm Rollback](https://helm.sh/docs/helm/helm_rollback/), Spec FR-023A/B

---

### Decision 8: Base Image Strategy

**Question**: Which base images for containers?

**Decision**: Alpine or distroless minimal images

**Rationale**:
- Smaller image size (<100MB frontend, <200MB backend)
- Reduced attack surface (fewer packages)
- Faster build and deployment times
- Meets spec requirements (FR-003, FR-006, FR-007)

**Alternatives Considered**:
- Ubuntu/Debian: Larger images, slower builds
- Full language images: Include build tools unnecessary for runtime

**References**: [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)

---

## Phase 1: Design

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Key Entities**:
- **Docker Image**: Frontend and backend container images with metadata
- **Kubernetes Deployment**: Replica sets, pod templates, update strategies
- **Kubernetes Service**: Service discovery (LoadBalancer, ClusterIP)
- **Helm Chart**: Package structure, values, templates
- **AI Agent**: kubectl-ai, kagent configurations and usage patterns
- **Pod**: Running containers with health status
- **ConfigMap/Secret**: Configuration and secret management

---

### Service Contracts

See [contracts/](./contracts/) directory for detailed API contracts.

**Frontend Service Contract** ([contracts/frontend-api.md](./contracts/frontend-api.md)):
- Endpoint: `http://127.0.0.1:3000` (via Minikube tunnel)
- Health check: `GET /health`
- Dependencies: Backend API for todo operations
- Environment variables: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_OPENAI_KEY`

**Backend Service Contract** ([contracts/backend-api.md](./contracts/backend-api.md)):
- Endpoint: `http://backend-service:8000` (ClusterIP)
- Health check: `GET /health`
- API endpoints: `/todos` (CRUD operations), `/chat` (AI chatbot)
- Environment variables: `DATABASE_URL`, `OPENAI_API_KEY`, `NEON_DB_URL`

**Health Check Contracts** ([contracts/health-checks.md](./contracts/health-checks.md)):
- Liveness probe: `GET /health` (10s interval, 5s timeout)
- Readiness probe: `GET /ready` (10s interval, 5s timeout)
- Startup probe: `GET /health` (10s interval, 5s timeout, 30s failure threshold)

---

### Quick Start Guide

See [quickstart.md](./quickstart.md) for complete deployment instructions.

**Workflow**:
1. **Prerequisites**: Install Docker Desktop, Minikube, kubectl, Helm, kubectl-ai, kagent
2. **Cluster Setup**: `minikube start --driver=docker --cpus=4 --memory=8192`
3. **Build Images**: `./scripts/build-images.sh`
4. **Deploy**: `helm install todo-chatbot ./helm -f helm/values-dev.yaml`
5. **Access**: `minikube tunnel` (separate terminal) → Open http://127.0.0.1:3000
6. **Test**: `./scripts/test-deployment.sh`
7. **Teardown**: `helm uninstall todo-chatbot` or `./scripts/teardown.sh`

**AI DevOps Workflow**:
- **Deploy**: `kubectl-ai deploy the todo chatbot with 2 replicas`
- **Scale**: `kubectl-ai scale the backend to 3 replicas`
- **Debug**: `kubectl-ai check why pods are failing`
- **Analyze**: `kagent analyze cluster health`

---

## Constitution Check (Post-Design)

### Re-evaluation of Gates

All 5 constitution gates remain **PASS** after design phase:

**Principle 10 (Spec-Driven Infrastructure)**:
✅ Helm chart structure provides clear spec-to-manifest mapping
✅ No manual Kubernetes YAML required

**Principle 11 (AI-Augmented DevOps)**:
✅ kubectl-ai/kagent integrated throughout deployment workflow
✅ Manual fallback documented in quickstart

**Principle 12 (Cloud-Native Best Practices)**:
✅ Data model includes HPA, rolling updates, health probes
✅ Service contracts follow Kubernetes patterns

**Principle 13 (Local Reproducibility)**:
✅ Quickstart provides complete local deployment steps
✅ Zero cloud dependencies, <10 minute deployment cycle

**Principle 14 (Infrastructure Observability)**:
✅ Health check contracts define liveness/readiness/startup probes
✅ kubectl and kagent usage documented throughout

---

## Implementation Tasks

### Task Breakdown

See [tasks.md](../tasks.md) for complete task list with dependencies.

**High-Level Tasks**:

1. **Phase 0 (Research)**: ✅ COMPLETE
   - [x] Evaluate container runtime options
   - [x] Choose Kubernetes distribution
   - [x] Define service exposure strategy
   - [x] Determine configuration management approach
   - [x] Decide AI automation level
   - [x] Define success criteria
   - [x] Specify rollback/teardown behavior

2. **Phase 1 (Design)**: ✅ COMPLETE
   - [x] Define data model entities
   - [x] Design service contracts
   - [x] Specify health check endpoints
   - [x] Create Helm chart structure
   - [x] Document quickstart workflow

3. **Phase 2 (Implementation)**: ⏳ PENDING
   - [ ] Create multi-stage Dockerfiles (frontend, backend)
   - [ ] Build and optimize Docker images
   - [ ] Create Helm chart templates
   - [ ] Write deployment scripts
   - [ ] Implement health check endpoints
   - [ ] Create environment-specific values files

4. **Phase 3 (AI DevOps Integration)**: ⏳ PENDING
   - [ ] Test kubectl-ai deployment
   - [ ] Test kubectl-ai scaling operations
   - [ ] Test kubectl-ai debugging
   - [ ] Test kagent cluster analysis
   - [ ] Document manual fallback procedures

5. **Phase 4 (Testing & Validation)**: ⏳ PENDING
   - [ ] Deploy on Minikube (fresh install)
   - [ ] Verify all pods Running and healthy
   - [ ] Test application functionality
   - [ ] Test rolling update (zero downtime)
   - [ ] Test Helm rollback
   - [ ] Test complete teardown and redeploy
   - [ ] Measure deployment time (<10 min)
   - [ ] Verify image size requirements
   - [ ] Document all acceptance scenarios

---

## Risks & Mitigations

### Risk 1: Minikube Resource Exhaustion

**Description**: Local machine may not have sufficient CPU/memory for Minikube cluster

**Impact**: High - Deployment fails, pods stuck in Pending state

**Mitigation**:
- Document minimum requirements (8GB RAM, 4 CPU cores)
- Provide resource tuning guide in quickstart
- Fallback to reduced replica count (1 per service)

**Monitoring**: `minikube status`, `kubectl top nodes`

---

### Risk 2: Docker Image Build Failures

**Description**: Multi-stage builds fail due to dependency issues or base image changes

**Impact**: High - Cannot deploy without images

**Mitigation**:
- Pin specific base image versions in Dockerfiles
- Use Docker build caching for faster rebuilds
- Provide build troubleshooting guide
- Fallback to pre-built images (if available)

**Monitoring**: Build logs, image size metrics

---

### Risk 3: kubectl-ai Generates Invalid Manifests

**Description**: AI agent generates incorrect Kubernetes YAML causing deployment failures

**Impact**: Medium - Primary deployment method fails, must use manual fallback

**Mitigation**:
- Validate AI-generated manifests before applying
- Provide manual kubectl/Helm commands as fallback
- Document common kubectl-ai errors and solutions
- Test kubectl-ai commands during development

**Monitoring**: Deployment logs, kubectl events

---

### Risk 4: Port Conflicts on Local Machine

**Description**: Ports 3000 or 8000 already in use by other applications

**Impact**: Medium - Services fail to start or become inaccessible

**Mitigation**:
- Document port requirements in quickstart
- Provide instructions for checking port usage (`netstat`, `lsof`)
- Allow configurable ports via Helm values
- Provide port conflict resolution guide

**Monitoring**: Service logs, Minikube tunnel status

---

### Risk 5: Backend Pod CrashLoopBackOff

**Description**: Backend pods fail to start due to missing environment variables or database connectivity

**Impact**: High - Application partially functional (frontend works, backend fails)

**Mitigation**:
- Document all required environment variables
- Provide ConfigMap/Secret setup instructions
- Add startup probes with failure thresholds
- Include pod troubleshooting guide (`kubectl logs`, `kubectl describe`)

**Monitoring**: Pod status, backend logs, health check failures

---

## Success Criteria Validation

### Measurable Outcomes

From [spec.md](./spec.md), success criteria and how this plan achieves them:

- **SC-001**: All pods Running AND health checks pass AND app accessible (within 10 min)
  - Plan: Helm deployment workflow with health check validation
  - Validation: `./scripts/test-deployment.sh` verifies all three conditions

- **SC-002**: Application accessible within 2 minutes of deployment completion
  - Plan: Minikube tunnel provides immediate LoadBalancer IP
  - Validation: Quickstart documents browser access steps

- **SC-003**: Helm install/upgrade/rollback with 100% reliability
  - Plan: Helm chart structure with RollingUpdate strategy
  - Validation: Phase 4 testing includes rolling update and rollback tests

- **SC-004**: kubectl-ai completes at least 3 different operations
  - Plan: Phase 3 AI DevOps integration tests kubectl-ai deploy/scale/debug
  - Validation: Test suite verifies all three operations succeed

- **SC-005**: kagent provides at least 1 meaningful insight
  - Plan: Phase 3 includes kagent cluster health analysis
  - Validation: Document kagent output (resource utilization, optimization opportunities)

- **SC-006**: Complete teardown and redeploy in under 10 minutes
  - Plan: Teardown script removes all resources cleanly
  - Validation: Time deployment cycle with `time ./scripts/teardown.sh && ./scripts/deploy.sh`

- **SC-007**: Frontend image <100MB compressed
  - Plan: Multi-stage build with alpine base, npm ci --only=production
  - Validation: `docker images` shows image size

- **SC-008**: Backend image <200MB compressed
  - Plan: Multi-stage build with python:3.13-slim, pip install --no-cache-dir
  - Validation: `docker images` shows image size

- **SC-009**: All pods pass health checks within 30 seconds
  - Plan: Startup probes with 30s failure threshold, liveness/readiness probes
  - Validation: `kubectl get pods` shows pods Ready within 30s

- **SC-010**: Rolling updates with zero service interruption
  - Plan: RollingUpdate strategy with maxSurge and maxUnavailable
  - Validation: Load test during rolling update, verify zero failed requests

---

## Next Steps

1. **Execute `/sp.tasks`**: Generate detailed task breakdown from this plan
2. **Create Dockerfiles**: Implement multi-stage builds for frontend and backend
3. **Build Helm Charts**: Create templated Kubernetes manifests
4. **Write Deployment Scripts**: Automate build, deploy, teardown, testing
5. **AI DevOps Testing**: Validate kubectl-ai and kagent workflows
6. **Documentation**: Complete quickstart guide with troubleshooting
7. **Acceptance Testing**: Execute all 4 user story acceptance scenarios

---

## References

- [Feature Specification](./spec.md)
- [Requirements Checklist](../checklists/requirements.md)
- [Constitution v3.0](../../../.specify/memory/constitution.md)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
