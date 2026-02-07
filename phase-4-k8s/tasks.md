# Tasks: Local Kubernetes Deployment for Todo AI Chatbot

**Input**: Design documents from `phase-4-k8s/specs/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Deployment validation tests included as smoke tests (no TDD for infrastructure)

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Docker**: `phase-4-k8s/docker/frontend/`, `phase-4-k8s/docker/backend/`
- **Helm**: `phase-4-k8s/helm/`, `phase-4-k8s/helm/templates/`
- **Kubernetes**: `phase-4-k8s/k8s/manifests/` (for reference)
- **Scripts**: `phase-4-k8s/scripts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory structure and verify prerequisites

- [ ] T001 Create phase-4-k8s directory structure: docker/, helm/, k8s/manifests, k8s/overlays, scripts/
- [ ] T002 Verify Docker Desktop is installed and running (docker --version)
- [ ] T003 Verify Minikube is installed (minikube version)
- [ ] T004 Verify kubectl is installed and configured (kubectl version --client)
- [ ] T005 Verify Helm is installed (helm version)
- [ ] T006 [P] Create frontend .dockerignore in phase-4-k8s/docker/frontend/.dockerignore
- [ ] T007 [P] Create backend .dockerignore in phase-4-k8s/docker/backend/.dockerignore
- [ ] T008 [P] Create Helm Chart.yaml in phase-4-k8s/helm/Chart.yaml
- [ ] T009 [P] Create Helm _helpers.tpl in phase-4-k8s/helm/templates/_helpers.tpl

**Checkpoint**: Directory structure created, all prerequisites verified, Helm scaffolding ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Docker and Helm infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Docker Images (Foundational for ALL user stories)

- [ ] T010 Create multi-stage Dockerfile for Next.js frontend in phase-4-k8s/docker/frontend/Dockerfile
  - Base: node:20-alpine (build stage), node:20-alpine (runtime stage)
  - EXPOSE 3000, CMD ["npm", "start"]
  - Non-root user (uid 1000), health check
  - .dockerignore optimization
  - Target size: <100MB compressed

- [ ] T011 Create multi-stage Dockerfile for FastAPI backend in phase-4-k8s/docker/backend/Dockerfile
  - Base: python:3.13-slim (build stage), python:3.13-slim (runtime stage)
  - EXPOSE 8000, CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  - Non-root user (uid 1000), health check
  - .dockerignore optimization
  - Target size: <200MB compressed

- [ ] T012 Build frontend Docker image: `docker build -t todo-chatbot-frontend:v1.0.0 phase-4-k8s/docker/frontend`
- [ ] T013 Build backend Docker image: `docker build -t todo-chatbot-backend:v1.0.0 phase-4-k8s/docker/backend`
- [ ] T014 Verify image sizes: `docker images | grep todo-chatbot` (frontend <100MB, backend <200MB)

### Helm Chart Structure (Foundational for ALL user stories)

- [ ] T015 Create Helm values.yaml (default configuration) in phase-4-k8s/helm/values.yaml
  - Namespace: todo-chatbot-dev
  - Replica counts: 2 (frontend), 2 (backend)
  - Resource requests/limits (CPU: 100m-200m, Memory: 128Mi-256Mi)
  - Image references: todo-chatbot-frontend:v1.0.0, todo-chatbot-backend:v1.0.0
  - Service types: LoadBalancer (frontend), ClusterIP (backend)

- [ ] T016 [P] Create Helm values-dev.yaml in phase-4-k8s/helm/values-dev.yaml
  - Override: namespace=todo-chatbot-dev, replicas=1
  - Lower resource limits for development
  - Debug log level

- [ ] T017 [P] Create Helm values-prod.yaml in phase-4-k8s/helm/values-prod.yaml
  - Override: namespace=todo-chatbot-prod, replicas=3
  - Standard resource limits for production-like
  - Info log level, HPA enabled

- [ ] T018 [P] Create ConfigMap template for frontend env in phase-4-k8s/helm/templates/frontend-configmap.yaml
  - NEXT_PUBLIC_API_URL, NEXT_PUBLIC_APP_NAME, NEXT_PUBLIC_ENVIRONMENT
  - Template helper for environment variable injection

- [ ] T019 [P] Create ConfigMap template for backend env in phase-4-k8s/helm/templates/backend-configmap.yaml
  - DATABASE_URL, LOG_LEVEL, API_PORT, CORS_ORIGINS
  - Template helper for environment variable injection

- [ ] T020 [P] Create Secret template for backend in phase-4-k8s/helm/templates/backend-secret.yaml
  - OPENAI_API_KEY (base64-encoded)
  - Template helper for secret reference

- [ ] T021 [P] Create frontend Deployment template in phase-4-k8s/helm/templates/frontend-deployment.yaml
  - Replica count from values, RollingUpdate strategy
  - Liveness/readiness/startup probes (/health:3000, /ready:3000)
  - Security context (non-root, read-only root fs)
  - Resource requests/limits, ConfigMap envFrom

- [ ] T022 [P] Create backend Deployment template in phase-4-k8s/helm/templates/backend-deployment.yaml
  - Replica count from values, RollingUpdate strategy
  - Liveness/readiness/startup probes (/health:8000, /ready:8000)
  - Security context (non-root, read-only root fs)
  - Resource requests/limits, ConfigMap envFrom, Secret envFrom

- [ ] T023 [P] Create frontend Service template (LoadBalancer) in phase-4-k8s/helm/templates/frontend-service.yaml
  - Type: LoadBalancer, port: 3000
  - Selector: app=frontend

- [ ] T024 [P] Create backend Service template (ClusterIP) in phase-4-k8s/helm/templates/backend-service.yaml
  - Type: ClusterIP, port: 8000
  - Selector: app=backend

- [ ] T025 [P] Create frontend HPA template in phase-4-k8s/helm/templates/frontend-hpa.yaml
  - Scale on CPU: 70%, Memory: 80%
  - Min replicas: 2, Max replicas: 10
  - Conditional: {{ .Values.frontend.hpa.enabled }}

- [ ] T026 [P] Create backend HPA template in phase-4-k8s/helm/templates/backend-hpa.yaml
  - Scale on CPU: 70%, Memory: 80%
  - Min replicas: 2, Max replicas: 10
  - Conditional: {{ .Values.backend.hpa.enabled }}

**Checkpoint**: Foundation ready - Docker images built, Helm chart complete, user story implementation can begin

---

## Phase 3: User Story 1 - Developer Deploys Chatbot Locally (Priority: P1) 🎯 MVP

**Goal**: Enable developer to deploy entire chatbot (frontend + backend) on Minikube and access via local URL

**Independent Test**:
1. Deploy with Helm: `helm install todo-chatbot ./helm -f values-dev.yaml -n todo-chatbot-dev`
2. Verify pods Running: `kubectl get pods -n todo-chatbot-dev` (all STATUS=Running, READY=1/1)
3. Start tunnel: `minikube tunnel` (separate terminal)
4. Access application: `curl http://127.0.0.1:3000/health` returns 200 OK
5. Test functionality: Chatbot interface loads and manages todos via natural language

### Deployment Scripts

- [ ] T027 [US1] Create Minikube setup script in phase-4-k8s/scripts/setup-minikube.sh
  - Start Minikube: `minikube start --driver=docker --cpus=4 --memory=8192`
  - Enable add-ons: dashboard, metrics-server
  - Create namespace: `kubectl create namespace todo-chatbot-dev`
  - Validate cluster: `kubectl get nodes`

- [ ] T028 [US1] Create image build script in phase-4-k8s/scripts/build-images.sh
  - Build frontend: `docker build -t todo-chatbot-frontend:v1.0.0 phase-4-k8s/docker/frontend`
  - Build backend: `docker build -t todo-chatbot-backend:v1.0.0 phase-4-k8s/docker/backend`
  - Load into Minikube: `minikube image load todo-chatbot-frontend:v1.0.0` and backend
  - Verify images: `docker images | grep todo-chatbot`

- [ ] T029 [US1] Create deployment script in phase-4-k8s/scripts/deploy.sh
  - Create OpenAI secret: `kubectl create secret generic backend-secrets --from-literal=OPENAI_API_KEY=...`
  - Create DB URL secret: `kubectl create secret generic backend-config --from-literal=DATABASE_URL=...`
  - Install Helm: `helm install todo-chatbot ./helm -f values-dev.yaml -n todo-chatbot-dev --wait`
  - Wait for rollout: `kubectl rollout status deployment/frontend -n todo-chatbot-dev`
  - Display access instructions

- [ ] T030 [US1] Create smoke test script in phase-4-k8s/scripts/test-deployment.sh
  - Check pod status: `kubectl get pods -n todo-chatbot-dev`
  - Check health endpoints: `kubectl exec -n todo-chatbot-dev frontend-xxx -- curl -s http://localhost:3000/health`
  - Port-forward backend: `kubectl port-forward -n todo-chatbot-dev backend-xxx 8000:8000`
  - Test backend health: `curl http://localhost:8000/health`
  - Test frontend access: `curl http://127.0.0.1:3000` (requires minikube tunnel)
  - Display results

- [ ] T031 [US1] Create teardown script in phase-4-k8s/scripts/teardown.sh
  - Uninstall Helm: `helm uninstall todo-chatbot -n todo-chatbot-dev`
  - Delete namespace: `kubectl delete namespace todo-chatbot-dev`
  - Verify cleanup: `kubectl get all -n todo-chatbot-dev`
  - Optional: `minikube delete` for complete reset

### Health Check Endpoints (Application Code)

- [ ] T032 [P] [US1] Add /health endpoint to Next.js frontend in phase-3-chatbot/frontend/app/api/health/route.ts
  - Return: { status: "healthy", timestamp: ISO, uptime: seconds }
  - HTTP 200 OK

- [ ] T033 [P] [US1] Add /ready endpoint to Next.js frontend in phase-3-chatbot/frontend/app/api/ready/route.ts
  - Check backend connectivity: `fetch(http://backend-service:8000/health)`
  - Return: { status: "ready", dependencies: { backend: "healthy" } }
  - HTTP 200 OK if backend healthy, 503 Service Unavailable if not

- [ ] T034 [P] [US1] Add /health endpoint to FastAPI backend in phase-3-chatbot/backend/main.py
  - Return: { status: "healthy", timestamp: ISO, uptime: seconds, database: "connected" }
  - Check database connection
  - HTTP 200 OK

- [ ] T035 [P] [US1] Add /ready endpoint to FastAPI backend in phase-3-chatbot/backend/main.py
  - Check database connectivity
  - Check OpenAI API key validity
  - Return: { status: "ready", dependencies: { database: "connected", openai: "authenticated" } }
  - HTTP 200 OK if all ready, 503 Service Unavailable if not

### Documentation

- [ ] T036 [US1] Create quickstart guide in phase-4-k8s/README.md
  - Prerequisites checklist
  - Step-by-step deployment (12 steps from quickstart.md)
  - Troubleshooting common issues
  - Link to detailed quickstart.md in specs/

**Checkpoint**: At this point, developer can deploy chatbot locally and access via http://127.0.0.1:3000 (MVP COMPLETE!)

---

## Phase 4: User Story 2 - Developer Uses AI Agents for Deployment Operations (Priority: P2)

**Goal**: Enable developer to use kubectl-ai and kagent for deployment, scaling, and cluster analysis

**Independent Test**:
1. Deploy with kubectl-ai: `kubectl-ai deploy the todo chatbot frontend with 2 replicas using image todo-chatbot-frontend:v1.0.0`
2. Verify deployment: `kubectl get deployment frontend -n todo-chatbot-dev` (2 replicas ready)
3. Scale with kubectl-ai: `kubectl-ai scale the backend deployment to 3 replicas`
4. Verify scaling: `kubectl get pods -n todo-chatbot-dev -l app=backend` (3 pods running)
5. Analyze with kagent: `kagent analyze cluster health in namespace todo-chatbot-dev`
6. Verify insights: kagent provides resource utilization and optimization suggestions

### kubectl-ai Integration

- [ ] T037 [P] [US2] Create kubectl-ai deployment guide in phase-4-k8s/docs/kubectl-ai-guide.md
  - Installation: `npm install -g kubectl-ai`
  - Configuration: `kubectl-ai config set openai_api_key`
  - Prompts for deployment, scaling, debugging
  - Manual fallback commands

- [ ] T038 [P] [US2] Test kubectl-ai deployment command in phase-4-k8s/scripts/test-kubectl-ai-deploy.sh
  - Deploy frontend: `kubectl-ai deploy the todo chatbot frontend with 2 replicas using image todo-chatbot-frontend:v1.0.0`
  - Deploy backend: `kubectl-ai deploy the todo chatbot backend with 2 replicas using image todo-chatbot-backend:v1.0.0`
  - Create services: `kubectl-ai create a LoadBalancer service for the frontend on port 3000`
  - Validate: `kubectl get all -n todo-chatbot-dev`

- [ ] T039 [US2] Test kubectl-ai scaling command in phase-4-k8s/scripts/test-kubectl-ai-scale.sh
  - Scale backend: `kubectl-ai scale the backend deployment to 3 replicas`
  - Scale frontend: `kubectl-ai scale the frontend deployment to 3 replicas`
  - Validate: `kubectl get pods -n todo-chatbot-dev`
  - Reset to 2 replicas: `kubectl scale deployment backend --replicas=2 -n todo-chatbot-dev`

- [ ] T040 [US2] Test kubectl-ai debugging command in phase-4-k8s/scripts/test-kubectl-ai-debug.sh
  - Intentionally break deployment (invalid image)
  - Run: `kubectl-ai check why the frontend pods are failing`
  - Validate: kubectl-ai identifies issue and provides solution
  - Fix deployment and verify recovery

### kagent Integration

- [ ] T041 [P] [US2] Create kagent analysis guide in phase-4-k8s/docs/kagent-guide.md
  - Installation: `npm install -g kagent`
  - Configuration: OpenAI API key setup
  - Prompts for health analysis, resource utilization, optimization
  - Manual fallback: `kubectl top pods`, `kubectl top nodes`

- [ ] T042 [US2] Test kagent cluster health analysis in phase-4-k8s/scripts/test-kagent-health.sh
  - Deploy application (use scripts from US1)
  - Run: `kagent analyze cluster health in namespace todo-chatbot-dev`
  - Validate: kagent provides health report (pod status, resource usage)
  - Verify actionable insights

- [ ] T043 [US2] Test kagent resource utilization in phase-4-k8s/scripts/test-kagent-resources.sh
  - Run: `kagent check CPU and memory usage for all pods in todo-chatbot-dev`
  - Validate: kagent displays resource consumption
  - Compare with: `kubectl top pods -n todo-chatbot-dev`

- [ ] T044 [US2] Test kagent optimization suggestions in phase-4-k8s/scripts/test-kagent-optimize.sh
  - Run: `kagent suggest optimizations for resource usage in namespace todo-chatbot-dev`
  - Validate: kagent provides optimization recommendations
  - Document suggestions in phase-4-k8s/docs/optimization-report.md

### Documentation Updates

- [ ] T045 [US2] Update quickstart.md with AI DevOps section in phase-4-k8s/specs/quickstart.md
  - Add Step 8: Scale with kubectl-ai
  - Add Step 9: Analyze with kagent
  - Document manual fallback procedures
  - Add AI agent troubleshooting

**Checkpoint**: At this point, developer can deploy and manage chatbot using kubectl-ai and kagent (AI-augmented DevOps COMPLETE!)

---

## Phase 5: User Story 3 - Developer Updates Application Using Helm (Priority: P3)

**Goal**: Enable developer to update application (new image version) using Helm with rolling updates and rollback

**Independent Test**:
1. Deploy initial version: `helm install todo-chatbot ./helm -f values-dev.yaml -n todo-chatbot-dev`
2. Upgrade to v1.0.1: `helm upgrade todo-chatbot ./helm -f values-dev.yaml --set frontend.image.tag=v1.0.1 -n todo-chatbot-dev --wait`
3. Verify rolling update: `kubectl rollout status deployment/frontend -n todo-chatbot-dev` (zero downtime)
4. Test during update: Continuous curl to http://127.0.0.1:3000/health (all requests succeed)
5. Rollback if needed: `helm rollback todo-chatbot 1 -n todo-chatbot-dev`
6. Verify rollback: System restored to previous working state

### Helm Upgrade & Rollback

- [ ] T046 [P] [US3] Create Helm upgrade script in phase-4-k8s/scripts/upgrade.sh
  - Accept version argument: `./upgrade.sh v1.0.1`
  - Upgrade: `helm upgrade todo-chatbot ./helm -f values-dev.yaml --set frontend.image.tag=$VERSION --set backend.image.tag=$VERSION -n todo-chatbot-dev --wait`
  - Monitor rolling update: `kubectl rollout status deployment/frontend -n todo-chatbot-dev`
  - Display upgrade status

- [ ] T047 [US3] Create rolling update validation script in phase-4-k8s/scripts/test-rolling-update.sh
  - Start continuous health check in background: `while true; do curl -s http://127.0.0.1:3000/health | jq .; sleep 1; done`
  - Run upgrade: `./upgrade.sh v1.0.1`
  - Verify: All health checks pass during update (zero failed requests)
  - Stop continuous health check
  - Display results

- [ ] T048 [US3] Create Helm rollback script in phase-4-k8s/scripts/rollback.sh
  - List revisions: `helm history todo-chatbot -n todo-chatbot-dev`
  - Accept revision argument: `./rollback.sh 1` (rollback to revision 1)
  - Rollback: `helm rollback todo-chatbot $REVISION -n todo-chatbot-dev`
  - Wait for rollout: `kubectl rollout status deployment/frontend -n todo-chatbot-dev`
  - Verify: Application works identically to previous state

- [ ] T049 [US3] Test environment-specific deployments in phase-4-k8s/scripts/test-environments.sh
  - Deploy dev: `helm install todo-chatbot-dev ./helm -f values-dev.yaml -n todo-chatbot-dev`
  - Verify: replicas=1, resources minimal, log level=debug
  - Uninstall: `helm uninstall todo-chatbot-dev -n todo-chatbot-dev`
  - Deploy prod: `helm install todo-chatbot-prod ./helm -f values-prod.yaml -n todo-chatbot-prod`
  - Verify: replicas=3, resources standard, log level=info, HPA enabled
  - Uninstall: `helm uninstall todo-chatbot-prod -n todo-chatbot-prod`

### Helm Chart Testing

- [ ] T050 [P] [US3] Create Helm chart linting in phase-4-k8s/scripts/test-helm-lint.sh
  - Lint chart: `helm lint ./helm`
  - Validate templates: `helm template todo-chatbot ./helm -f values-dev.yaml`
  - Dry-run install: `helm install todo-chatbot ./helm -f values-dev.yaml -n todo-chatbot-dev --dry-run --debug`
  - Display validation results

- [ ] T051 [US3] Create Helm chart installation test in phase-4-k8s/scripts/test-helm-install.sh
  - Clean environment: Delete namespace if exists
  - Install: `helm install todo-chatbot ./helm -f values-dev.yaml -n todo-chatbot-dev`
  - Verify: `helm status todo-chatbot -n todo-chatbot-dev`
  - Verify: All pods Running, services accessible
  - Validate: Health checks pass
  - Uninstall: `helm uninstall todo-chatbot -n todo-chatbot-dev`

- [ ] T052 [US3] Document Helm chart usage in phase-4-k8s/docs/helm-usage.md
  - Installation guide
  - Upgrade procedures
  - Rollback procedures
  - Values override examples
  - Troubleshooting common Helm issues

**Checkpoint**: At this point, developer can upgrade and rollback application using Helm with zero downtime

---

## Phase 6: User Story 4 - Developer Reproduces Deployment from Scratch (Priority: P4)

**Goal**: Validate spec-driven infrastructure automation - deployment is reproducible from specifications alone

**Independent Test**:
1. Start with clean Minikube: `minikube delete && minikube start --driver=docker --cpus=4 --memory=8192`
2. Deploy from specs: Follow quickstart.md exactly, using only Helm charts and values from phase-4-k8s/
3. Verify deployment: All pods Running, health checks pass, application accessible
4. Test functionality: Chatbot works identically to previous deployment
5. Teardown: `./scripts/teardown.sh` (all resources removed cleanly)
6. Redeploy: Repeat step 2-4, achieving identical working state

### Reproducibility Validation

- [ ] T053 [P] [US4] Create end-to-end reproducibility test in phase-4-k8s/scripts/test-reproducibility.sh
  - Clean Minikube: `minikube delete && minikube start --driver=docker --cpus=4 --memory=8192`
  - Deploy: `./scripts/deploy.sh` (from US1)
  - Verify: `./scripts/test-deployment.sh` passes
  - Teardown: `./scripts/teardown.sh`
  - Redeploy: `./scripts/deploy.sh` again
  - Re-verify: `./scripts/test-deployment.sh` passes
  - Display: Deployment time (<10 min required)

- [ ] T054 [US4] Create specification-only deployment guide in phase-4-k8s/docs/spec-driven-deployment.md
  - Deploy using ONLY specification documents (spec.md, plan.md, quickstart.md)
  - No external knowledge required
  - Step-by-step from specs to running application
  - Validate: Complete deployment achievable from specs alone

- [ ] T055 [US4] Create configuration comparison script in phase-4-k8s/scripts/test-identical-config.sh
  - Deploy first time: `./scripts/deploy.sh`
  - Export configuration: `kubectl get all -n todo-chatbot-dev -o yaml > deployment1.yaml`
  - Teardown and redeploy: `./scripts/teardown.sh && ./scripts/deploy.sh`
  - Export configuration: `kubectl get all -n todo-chatbot-dev -o yaml > deployment2.yaml`
  - Compare: `diff deployment1.yaml deployment2.yaml` (only timestamps should differ)
  - Display: Configuration is identical

- [ ] T056 [US4] Validate spec completeness in phase-4-k8s/scripts/test-spec-completeness.sh
  - Check: All required secrets documented in spec (FR-045)
  - Check: All environment variables specified (FR-044)
  - Check: All health checks defined (FR-042)
  - Check: Resource limits configured (FR-012)
  - Check: Replicas meet minimum (FR-011)
  - Display: Spec completeness report

### Documentation Validation

- [ ] T057 [US4] Create deployment verification checklist in phase-4-k8s/docs/deployment-checklist.md
  - Prerequisites verified
  - Minikube running
  - Docker images built and loaded
  - Secrets created
  - Helm chart installed
  - Pods Running and Ready
  - Health checks passing
  - Application accessible
  - Functionality tested

- [ ] T058 [US4] Update README with reproducibility section in phase-4-k8s/README.md
  - Add: "Reproduce from Scratch" section
  - Link to spec-driven-deployment.md
  - Link to deployment-checklist.md
  - Document: <10 min deployment goal

**Checkpoint**: At this point, deployment is fully reproducible from specifications alone (spec-driven automation COMPLETE!)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories, final validation

### Performance Optimization

- [ ] T059 [P] Optimize Docker image sizes in phase-4-k8s/docker/frontend/Dockerfile and phase-4-k8s/docker/backend/Dockerfile
  - Verify: frontend <100MB compressed (FR-006, SC-007)
  - Verify: backend <200MB compressed (FR-007, SC-008)
  - Multi-stage build optimization
  - .dockerignore refinement

- [ ] T060 [P] Measure deployment performance in phase-4-k8s/scripts/test-performance.sh
  - Time: `time ./scripts/deploy.sh` (target: <10 min per SC-001, SC-006)
  - Time: Pod startup (target: <30s per SC-009)
  - Time: Rolling update (target: <2 min per SC-010)
  - Display: Performance metrics report

- [ ] T061 [P] Optimize Helm template rendering in phase-4-k8s/helm/templates/_helpers.tpl
  - Add reusable template helpers
  - Reduce template complexity
  - Validate: `helm template` renders quickly

### Security Hardening

- [ ] T062 [P] Validate security context in phase-4-k8s/scripts/test-security.sh
  - Verify: Frontend runs as non-root (FR-004)
  - Verify: Backend runs as non-root (FR-004)
  - Verify: Read-only root filesystem (FR-015)
  - Verify: No secrets in ConfigMaps (only in Secrets)
  - Display: Security validation report

- [ ] T063 [P] Scan Docker images for vulnerabilities in phase-4-k8s/scripts/test-vulnerability-scan.sh
  - Run: `docker scan todo-chatbot-frontend:v1.0.0` (if available)
  - Run: `docker scan todo-chatbot-backend:v1.0.0` (if available)
  - Display: Vulnerability report

### Documentation & Guides

- [ ] T064 [P] Create comprehensive troubleshooting guide in phase-4-k8s/docs/troubleshooting.md
  - Minikube issues (resource exhaustion, node not ready)
  - Docker issues (build failures, image pull errors)
  - Helm issues (chart installation failures, upgrade failures)
  - Pod issues (CrashLoopBackOff, ImagePullBackOff)
  - Network issues (LoadBalancer not accessible, port conflicts)
  - AI agent issues (kubectl-ai errors, kagent errors)
  - Solutions and workarounds for each issue

- [ ] T065 [P] Create development workflow guide in phase-4-k8s/docs/development-workflow.md
  - Rapid iteration cycle (<5 min per FR-036)
  - Code → Build → Deploy → Test workflow
  - Hot reload vs full deployment
  - Debugging pods and services
  - Local development tips

- [ ] T066 Update main README with complete documentation in phase-4-k8s/README.md
  - Overview and features
  - Quick start (link to quickstart.md)
  - AI DevOps (link to kubectl-ai-guide.md, kagent-guide.md)
  - Helm usage (link to helm-usage.md)
  - Troubleshooting (link to troubleshooting.md)
  - Architecture diagram

### Final Validation

- [ ] T067 Run complete acceptance test suite in phase-4-k8s/scripts/test-all.sh
  - Run US1 tests: Deploy and access application
  - Run US2 tests: kubectl-ai and kagent operations
  - Run US3 tests: Helm upgrade and rollback
  - Run US4 tests: Reproducibility validation
  - Run performance tests: Deployment time, image sizes
  - Run security tests: Non-root, read-only fs
  - Display: Complete test results report

- [ ] T068 Validate all success criteria from spec.md in phase-4-k8s/scripts/test-success-criteria.sh
  - SC-001: All pods Running + health checks pass + app accessible (<10 min)
  - SC-002: Application accessible within 2 min of deployment
  - SC-003: Helm install/upgrade/rollback with 100% reliability
  - SC-004: kubectl-ai completes 3 different operations
  - SC-005: kagent provides meaningful insight
  - SC-006: Teardown and redeploy in under 10 min
  - SC-007: Frontend image <100MB
  - SC-008: Backend image <200MB
  - SC-009: Pods pass health checks within 30s
  - SC-010: Rolling update with zero service interruption
  - Display: Success criteria validation report

**Checkpoint**: All user stories complete, validated, polished - Phase IV ready for demo!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T009) - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase (T010-T026) completion
  - US1 (Phase 3): Core deployment capability
  - US2 (Phase 4): AI DevOps integration - can run in parallel with US3/US4 after US1
  - US3 (Phase 5): Helm workflows - can run in parallel with US2/US4 after US1
  - US4 (Phase 6): Reproducibility validation - can run in parallel with US2/US3 after US1
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Phase 3)**: Can start after Foundational (T010-T026) - No dependencies on other stories
  - **BLOCKS**: US2, US3, US4 (all require deployed application)
  - **Checkpoint**: MVP complete after US1

- **User Story 2 (P2 - Phase 4)**: Depends on US1 completion (T027-T036)
  - Requires: Deployed application to test kubectl-ai and kagent
  - Can run in parallel with US3 and US4

- **User Story 3 (P3 - Phase 5)**: Depends on US1 completion (T027-T036)
  - Requires: Deployed application to test Helm upgrades
  - Can run in parallel with US2 and US4

- **User Story 4 (P4 - Phase 6)**: Depends on US1 completion (T027-T036)
  - Requires: Deployed application to test reproducibility
  - Can run in parallel with US2 and US3

### Within Each Phase

- **Setup (Phase 1)**: T001-T005 sequential (prerequisites), T006-T009 parallel (file creation)
- **Foundational (Phase 2)**:
  - T010-T011 sequential (Dockerfiles must be created before building)
  - T012-T014 sequential (build must complete before verification)
  - T015-T017 parallel (different values files)
  - T018-T020 parallel (ConfigMaps and Secret templates)
  - T021-T026 parallel (Deployment, Service, HPA templates)
- **User Story 1 (Phase 3)**:
  - T027-T031 sequential (scripts build on each other)
  - T032-T035 parallel (health check endpoints in different services)
  - T036 sequential (documentation depends on scripts)
- **User Story 2 (Phase 4)**:
  - T037-T038 parallel (deployment guide and test script)
  - T039 sequential (scaling test depends on deployment)
  - T040 sequential (debugging test intentionally breaks deployment)
  - T041-T042 parallel (kagent guide and health test)
  - T043-T044 sequential (resource test before optimization)
  - T045 sequential (documentation update)
- **User Story 3 (Phase 5)**:
  - T046-T047 sequential (upgrade before rolling update test)
  - T048 sequential (rollback test)
  - T049 sequential (environment test)
  - T050-T051 sequential (lint before install test)
  - T052 sequential (documentation)
- **User Story 4 (Phase 6)**:
  - T053 sequential (reproducibility test is end-to-end)
  - T054-T055 sequential (spec guide before config comparison)
  - T056 sequential (spec completeness test)
  - T057-T058 sequential (checklist before README update)
- **Polish (Phase 7)**:
  - T059-T061 parallel (optimization tasks)
  - T062-T063 parallel (security tasks)
  - T064-T066 parallel (documentation tasks)
  - T067-T068 sequential (final validation depends on all)

### Parallel Opportunities

**Setup Phase (Phase 1)**:
```bash
# Can run in parallel (different files):
Task T006: Create frontend .dockerignore
Task T007: Create backend .dockerignore
Task T008: Create Helm Chart.yaml
Task T009: Create Helm _helpers.tpl
```

**Foundational Phase (Phase 2)**:
```bash
# Can run in parallel (different values files):
Task T016: Create values-dev.yaml
Task T017: Create values-prod.yaml

# Can run in parallel (different templates):
Task T018: Frontend ConfigMap template
Task T019: Backend ConfigMap template
Task T020: Backend Secret template
Task T021: Frontend Deployment template
Task T022: Backend Deployment template
Task T023: Frontend Service template
Task T024: Backend Service template
Task T025: Frontend HPA template
Task T026: Backend HPA template
```

**User Story 1 (Phase 3)**:
```bash
# Can run in parallel (different services):
Task T032: Frontend /health endpoint
Task T033: Frontend /ready endpoint
Task T034: Backend /health endpoint
Task T035: Backend /ready endpoint
```

**User Story 2 (Phase 4)**:
```bash
# Can run in parallel (different AI agents):
Task T037: kubectl-ai guide
Task T038: kubectl-ai deployment test
Task T041: kagent guide
Task T042: kagent health test
```

**Polish Phase (Phase 7)**:
```bash
# Can run in parallel (independent improvements):
Task T059: Optimize Docker images
Task T060: Measure performance
Task T061: Optimize Helm templates
Task T062: Validate security context
Task T063: Scan for vulnerabilities
Task T064: Troubleshooting guide
Task T065: Development workflow guide
Task T066: Update README
```

---

## Parallel Example: User Story 1 (US1)

```bash
# After Foundational phase completes, launch US1 health check endpoints together:
Task: "Add /health endpoint to Next.js frontend in phase-3-chatbot/frontend/app/api/health/route.ts"
Task: "Add /ready endpoint to Next.js frontend in phase-3-chatbot/frontend/app/api/ready/route.ts"
Task: "Add /health endpoint to FastAPI backend in phase-3-chatbot/backend/main.py"
Task: "Add /ready endpoint to FastAPI backend in phase-3-chatbot/backend/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Goal**: Get to working deployment as fast as possible

1. Complete Phase 1: Setup (T001-T009) - ~30 min
2. Complete Phase 2: Foundational (T010-T026) - ~2 hours
   - Build Docker images
   - Create Helm chart
3. Complete Phase 3: User Story 1 (T027-T036) - ~2 hours
   - Create deployment scripts
   - Add health check endpoints
   - Write documentation
4. **STOP and VALIDATE**: Deploy on Minikube, test application works
5. **MVP COMPLETE!**: Deploy/demo local Kubernetes chatbot

**Total Time to MVP**: ~4-5 hours

### Incremental Delivery (Recommended)

1. **Iteration 1**: Setup + Foundational + US1 → Working deployment (MVP)
2. **Iteration 2**: Add US2 → AI DevOps capabilities (kubectl-ai, kagent)
3. **Iteration 3**: Add US3 → Helm workflows (upgrade, rollback)
4. **Iteration 4**: Add US4 → Reproducibility validation
5. **Iteration 5**: Polish → Performance, security, documentation

**Each iteration adds value without breaking previous iterations**

### Parallel Team Strategy

With multiple developers (after Foundational phase):

1. **Developer A**: User Story 1 (deployment scripts, health endpoints)
2. **Developer B**: User Story 2 (kubectl-ai, kagent integration) - waits for US1
3. **Developer C**: User Story 3 (Helm workflows) - waits for US1
4. **Developer D**: User Story 4 (reproducibility) - waits for US1

**All stories integrate cleanly after US1 completes**

---

## Task Summary

| Phase | Tasks | Focus | Estimated Time |
|-------|-------|-------|----------------|
| **Phase 1: Setup** | T001-T009 (9 tasks) | Directory structure, prerequisites | 30 min |
| **Phase 2: Foundational** | T010-T026 (17 tasks) | Docker images, Helm chart | 2 hours |
| **Phase 3: US1** | T027-T036 (10 tasks) | Deploy locally | 2 hours |
| **Phase 4: US2** | T037-T045 (9 tasks) | AI DevOps (kubectl-ai, kagent) | 2 hours |
| **Phase 5: US3** | T046-T052 (7 tasks) | Helm workflows (upgrade, rollback) | 1.5 hours |
| **Phase 6: US4** | T053-T058 (6 tasks) | Reproducibility validation | 1.5 hours |
| **Phase 7: Polish** | T059-T068 (10 tasks) | Optimization, documentation, validation | 2 hours |
| **Total** | **68 tasks** | **Complete Phase IV** | **~11.5 hours** |

**MVP (Phases 1-3)**: 36 tasks, ~4.5 hours → Working local deployment!

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** = maps task to specific user story for traceability
- **Each user story independently completable and testable**
- **Stop at any checkpoint to validate story independently**
- **Commit after each task or logical group**
- **MVP after Phase 3**: Working local deployment (US1)
- **Incremental delivery**: Add US2, US3, US4 one at a time
- **Avoid**: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ Task IDs sequential: T001-T068
✅ Parallel tasks marked with [P]
✅ User story tasks marked with [US1], [US2], [US3], [US4]
✅ Setup tasks have no story label
✅ Foundational tasks have no story label
✅ Polish tasks have no story label
✅ All file paths explicit and absolute
✅ All tasks independently executable
✅ All user stories independently testable
