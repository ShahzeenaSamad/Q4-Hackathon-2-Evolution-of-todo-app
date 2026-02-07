# Data Model: Local Kubernetes Deployment for Todo AI Chatbot

**Feature**: Phase IV - Local Kubernetes Deployment
**Phase**: Phase 1 (Design)
**Date**: 2026-01-30
**Status**: Complete

## Overview

This document defines the core entities for the Phase IV local Kubernetes deployment system. These entities represent the infrastructure components, their relationships, and their role in the overall deployment architecture.

---

## Core Entities

### 1. Docker Image

**Description**: Executable package containing application code and dependencies

**Attributes**:
- `name`: string (e.g., "todo-chatbot-frontend", "todo-chatbot-backend")
- `tag`: string (e.g., "v1.0.0", "latest")
- `base_image`: string (e.g., "node:20-alpine", "python:3.13-slim")
- `size_bytes`: integer (compressed image size)
- `architecture`: string (e.g., "amd64", "arm64")
- `created_at`: timestamp
- `ports`: number[] (exposed ports: [3000] for frontend, [8000] for backend)
- `health_check`: object (HEALTHCHECK configuration)
- `run_as_non_root`: boolean (security setting)
- `read_only_root_fs`: boolean (security setting)

**Relationships**:
- Used by: Kubernetes Deployment (pod template)
- Built from: Dockerfile

**Validation Rules**:
- Frontend size < 100MB (FR-006)
- Backend size < 200MB (FR-007)
- Must include health check (FR-005)
- Must run as non-root (FR-004)

---

### 2. Kubernetes Deployment

**Description**: Declarative specification for managing replicated pods

**Attributes**:
- `name`: string (e.g., "frontend", "backend")
- `namespace`: string (e.g., "todo-chatbot-dev", "todo-chatbot-prod")
- `replicas`: integer (minimum 2 per FR-011)
- `selector`: object (label selector for pods)
- `strategy`: string (RollingUpdate per FR-014)
- `min_ready_seconds`: integer (time before pod considered ready)
- `revision_history_limit`: integer (number of old replica sets to keep)

**Pod Template** (embedded):
- `containers`: Container[]
- `restart_policy`: string (Always)
- `dns_policy`: string (ClusterFirst)
- `security_context`: object (non-root, read-only root fs per FR-015)

**Container** (embedded):
- `name`: string
- `image`: string (Docker Image reference)
- `ports`: object[] (container ports)
- `env`: object[] (environment variables from ConfigMap/Secret)
- `resources`: object (requests and limits per FR-012)
- `liveness_probe`: object (HTTP GET per FR-013)
- `readiness_probe`: object (HTTP GET per FR-013)
- `startup_probe`: object (HTTP GET per FR-013)

**Relationships**:
- Creates: Kubernetes Pods
- Uses: Docker Image
- Configured by: Helm Chart (deployment template)
- Monitored by: HorizontalPodAutoscaler

**Validation Rules**:
- Minimum 2 replicas (FR-011)
- Resource requests and limits must be set (FR-012)
- Liveness, readiness, and startup probes required (FR-013)
- RollingUpdate strategy required (FR-014)
- Security context: non-root, read-only root filesystem (FR-015)

---

### 3. Kubernetes Pod

**Description**: Smallest deployable Kubernetes unit (one or more containers)

**Attributes**:
- `name`: string (auto-generated, e.g., "frontend-7d9f8d5c-k4m2x")
- `namespace`: string
- `phase`: string (Pending, Running, Succeeded, Failed, Unknown)
- `pod_ip`: string (cluster IP address)
- `node_name`: string (Minikube node)
- `start_time`: timestamp
- `labels`: object (app, version, etc.)

**Container Status** (embedded array):
- `name`: string
- `ready`: boolean
- `restart_count`: integer
- `image`: string
- `image_id`: string
- `state`: object (running, waiting, terminated)
- `last_state`: object (previous container state)

**Relationships**:
- Managed by: Kubernetes Deployment
- Contains: Container(s)
- Exposed by: Kubernetes Service
- Monitored by: Probes (liveness, readiness, startup)

**Validation Rules**:
- Must reach Running phase within 30 seconds (SC-009)
- All containers must be ready=true
- Restart count should be 0 or low (no CrashLoopBackOff)
- Pod IP must be assigned

---

### 4. Kubernetes Service

**Description**: Network abstraction for pod-to-pod communication

**Attributes**:
- `name`: string (e.g., "frontend-service", "backend-service")
- `namespace`: string
- `type`: string (LoadBalancer for frontend, ClusterIP for backend)
- `cluster_ip`: string (internal cluster IP)
- `external_ip`: string (external LoadBalancer IP via Minikube tunnel)
- `ports`: object[] (service ports)
- `selector`: object (label selector for pods)
- `session_affinity`: string (None or ClientIP)

**Port Mapping** (embedded):
- `name`: string (e.g., "http")
- `protocol`: string (TCP)
- `port`: integer (service port)
- `target_port`: integer (container port)
- `node_port`: integer (for NodePort type)

**Relationships**:
- Routes to: Kubernetes Pods (via selector)
- Defined in: Helm Chart (service template)
- Accessed by: Users (frontend), Frontend (backend)

**Validation Rules**:
- Frontend: LoadBalancer type (accessible via Minikube tunnel)
- Backend: ClusterIP type (internal only)
- Selector must match pod labels
- At least one port defined

---

### 5. ConfigMap

**Description**: Configuration data for environment variables

**Attributes**:
- `name`: string (e.g., "frontend-config", "backend-config")
- `namespace`: string
- `data`: object (key-value pairs of environment variables)

**Environment Variables** (Frontend ConfigMap):
- `NEXT_PUBLIC_API_URL`: string (backend service URL)
- `NEXT_PUBLIC_APP_NAME`: string (application name)
- `NEXT_PUBLIC_ENVIRONMENT`: string (dev, staging, production)

**Environment Variables** (Backend ConfigMap):
- `DATABASE_URL`: string (Neon database connection string)
- `LOG_LEVEL`: string (debug, info, warn, error)
- `API_PORT`: string (8000)

**Relationships**:
- Used by: Kubernetes Deployment (envFrom)
- Defined in: Helm Chart (configmap template)
- Values from: Helm values files

**Validation Rules**:
- No secrets (use Secret instead)
- All values must be strings
- Must be referenced by Deployment

---

### 6. Secret

**Description**: Sensitive data (API keys, passwords)

**Attributes**:
- `name`: string (e.g., "backend-secrets")
- `namespace`: string
- `type`: string (Opaque)
- `data`: object (base64-encoded key-value pairs)

**Secret Data** (Backend Secret):
- `OPENAI_API_KEY`: string (base64-encoded)
- `NEON_DB_PASSWORD`: string (base64-encoded, if separate)

**Relationships**:
- Used by: Kubernetes Deployment (envFrom)
- Defined in: Helm Chart (secret template)
- Created via: kubectl or Helm --set

**Validation Rules**:
- All values must be base64-encoded
- Never logged in plain text
- Must be referenced by Deployment
- Not committed to git repository

---

### 7. HorizontalPodAutoscaler (HPA)

**Description**: Automatically scales deployment replicas based on CPU/memory

**Attributes**:
- `name`: string (e.g., "frontend-hpa", "backend-hpa")
- `namespace`: string
- `scale_target_ref`: object (deployment reference)
- `min_replicas`: integer (minimum 2 per FR-011)
- `max_replicas`: integer (maximum 10 per FR-037)
- `metrics`: object[] (CPU, memory)
- `behavior`: object (scaling stabilization)

**Metrics** (embedded array):
- `type`: string (Resource)
- `resource`: object (name: cpu/memory, target: percentage)

**Relationships**:
- Scales: Kubernetes Deployment
- Monitors: Kubernetes Pods (resource usage)
- Defined in: Helm Chart (hpa template)

**Validation Rules**:
- Min replicas: 2-3 (FR-011, FR-037)
- Max replicas: 10 (FR-037)
- Target CPU: 70% (FR-037)
- Target memory: 80% (FR-037)

---

### 8. Helm Chart

**Description**: Package of pre-configured Kubernetes resources

**Attributes**:
- `name`: string (e.g., "todo-chatbot")
- `version`: string (e.g., "1.0.0", follows SemVer)
- `description`: string (chart description)
- `app_version`: string (application version)
- `api_version`: string (v2 for Helm 3)
- `kube_version`: string (Kubernetes version constraint)

**Chart Structure**:
- `Chart.yaml`: Chart metadata
- `values.yaml`: Default configuration values
- `values-dev.yaml`: Development environment overrides
- `values-prod.yaml`: Production environment overrides
- `templates/_helpers.tpl`: Template helper functions
- `templates/frontend/*.yaml`: Frontend resources (deployment, service, hpa, configmap)
- `templates/backend/*.yaml`: Backend resources (deployment, service, hpa, configmap, secret)

**Relationships**:
- Contains: Kubernetes manifests (as templates)
- Configures: Deployments, Services, ConfigMaps, Secrets, HPA
- Installed via: Helm CLI or kubectl-ai

**Validation Rules**:
- Must install successfully on first attempt (FR-023)
- Must support environment-specific overrides (FR-019)
- Must use template helpers (FR-020)
- Must include all required templates (FR-021, FR-022)

---

### 9. Helm Values

**Description**: Configuration values for Helm chart templates

**Global Values**:
- `namespace`: string (default: "todo-chatbot-dev")
- `replicaCount`: integer (default: 2)
- `imagePullPolicy`: string (IfNotPresent)

**Frontend Values**:
- `frontend.image.repository`: string (todo-chatbot-frontend)
- `frontend.image.tag`: string (v1.0.0)
- `frontend.service.type`: string (LoadBalancer)
- `frontend.service.port`: integer (3000)
- `frontend.resources.requests.cpu`: string (100m)
- `frontend.resources.requests.memory`: string (128Mi)
- `frontend.resources.limits.cpu`: string (200m)
- `frontend.resources.limits.memory`: string (256Mi)
- `frontend.env.NEXT_PUBLIC_API_URL`: string (http://backend-service:8000)
- `frontend.hpa.enabled`: boolean (true for prod, false for dev)
- `frontend.hpa.minReplicas`: integer (2)
- `frontend.hpa.maxReplicas`: integer (10)

**Backend Values**:
- `backend.image.repository`: string (todo-chatbot-backend)
- `backend.image.tag`: string (v1.0.0)
- `backend.service.type`: string (ClusterIP)
- `backend.service.port`: integer (8000)
- `backend.resources.requests.cpu`: string (100m)
- `backend.resources.requests.memory`: string (128Mi)
- `backend.resources.limits.cpu`: string (200m)
- `backend.resources.limits.memory`: string (256Mi)
- `backend.env.DATABASE_URL`: string (Neon database URL)
- `backend.env.LOG_LEVEL`: string (info)
- `backend.secrets.OPENAI_API_KEY`: string (OpenAI API key)
- `backend.hpa.enabled`: boolean (true for prod, false for dev)
- `backend.hpa.minReplicas`: integer (2)
- `backend.hpa.maxReplicas`: integer (10)

**Relationships**:
- Configures: Helm Chart templates
- Overridden by: Environment-specific values files
- Passed via: Helm install --values or --set

**Validation Rules**:
- Must work for local Minikube (FR-047)
- Must support multiple environments (FR-046)
- All parameters must be documented (FR-048)

---

### 10. AI Agent (kubectl-ai, kagent)

**Description**: AI-powered Kubernetes operations and analysis

**kubectl-ai Agent**:
- `name`: string ("kubectl-ai")
- `purpose`: string ("Generate Kubernetes manifests from natural language")
- `operations`: string[] (deploy, scale, debug, create, update)
- `input_format`: string (natural language)
- `output_format`: string (kubectl commands or YAML manifests)

**kagent Agent**:
- `name`: string ("kagent")
- `purpose`: string ("Analyze cluster health and resource utilization")
- `operations`: string[] (health-check, resource-analysis, optimization-suggestions)
- `input_format`: string (natural language or kubectl commands)
- `output_format`: string (analysis report with insights)

**Relationships**:
- Used by: Developer (primary method per FR-029)
- Operates on: Kubernetes Cluster (Minikube)
- Fallback: Manual kubectl/Helm commands (FR-030)

**Validation Rules**:
- Must successfully complete deployment (FR-024)
- Must successfully complete scaling (FR-025)
- Must successfully provide debugging insights (FR-026)
- Must provide meaningful cluster analysis (FR-027, FR-028)
- Primary method for all operations (FR-029)

---

### 11. Minikube Cluster

**Description**: Local single-node Kubernetes environment

**Attributes**:
- `name`: string (minikube)
- `status`: string (Running, Stopped, Deleted)
- `driver`: string (docker)
- `cpus`: integer (4)
- `memory`: integer (8192 MB)
- `disk_size`: integer (20000 MB)
- `kubernetes_version`: string (e.g., "v1.32.0")
- `node_ip`: string (192.168.49.2 or similar)
- `endpoint`: string (https://192.168.49.2:8443)

**Add-ons**:
- `dashboard`: boolean (true)
- `metrics-server`: boolean (true)
- `tunnel`: boolean (true, provides LoadBalancer IPs)

**Relationships**:
- Hosts: Kubernetes Pods, Deployments, Services
- Managed by: kubectl (configured by Minikube)
- Accessed via: kubectl CLI, Minikube dashboard

**Validation Rules**:
- Minimum 8GB RAM, 4 CPUs (Assumptions)
- Docker driver required (Constraints)
- Tunnel must be running for LoadBalancer services

---

### 12. Namespace

**Description**: Logical cluster partition for resource isolation

**Attributes**:
- `name`: string (todo-chatbot-dev, todo-chatbot-prod)
- `status`: string (Active)
- `labels`: object (environment, app)
- `created_at`: timestamp

**Resources** (contained):
- Deployments
- Services
- ConfigMaps
- Secrets
- Pods
- HPAs

**Relationships**:
- Contains: All Kubernetes resources
- Isolates: Development vs production-like environments

**Environment Configurations**:

**Development (todo-chatbot-dev)**:
- Replicas: 1 per service
- Resource limits: Minimal (CPU: 100m-200m, Memory: 128Mi-256Mi)
- Log level: Debug
- HPA: Disabled

**Production-Like (todo-chatbot-prod)**:
- Replicas: 2-3 per service
- Resource limits: Standard (CPU: 250m-500m, Memory: 256Mi-512Mi)
- Log level: Info
- HPA: Enabled (2-10 replica range)

---

## Entity Relationships

```
[Minikube Cluster]
    |
    +--> [Namespace]
            |
            +--> [Helm Chart]
            |       |
            |       +--> [Helm Values]
            |       |
            |       +--> [Kubernetes Deployment]
            |       |       |
            |       |       +--> [Kubernetes Pod]
            |       |       |       |
            |       |       |       +--> [Container] --> [Docker Image]
            |       |       |
            |       |       +--> [HorizontalPodAutoscaler]
            |       |
            |       +--> [Kubernetes Service]
            |       |
            |       +--> [ConfigMap]
            |       |
            |       +--> [Secret]
            |
            +--> [AI Agent] (kubectl-ai, kagent)
```

---

## State Transitions

### Deployment Lifecycle

```
[Draft] --> [Building Images] --> [Helm Install] --> [Pods Pending] --> [Pods Running] --> [Health Checks Pass] --> [Application Accessible]
                  |                         |                    |                       |
                  |                         v                    v                       v
                  |                   [Rollback]          [CrashLoopBackOff]    [Failed]
                  |                         |                    |
                  +-------------------------+--------------------+
                  |
                  v
            [Teardown] --> [Resources Deleted]
```

### Scaling Operations

```
[Current State: 2 Replicas]
        |
        v
[kubectl-ai: "scale to 3 replicas"] OR [HPA triggers]
        |
        v
[Deployment Updated]
        |
        v
[New Pod Created] --> [Pod Starting] --> [Pod Ready]
        |
        v
[Current State: 3 Replicas]
```

---

## Validation Summary

**Size Constraints**:
- Frontend Docker image < 100MB (FR-006, SC-007)
- Backend Docker image < 200MB (FR-007, SC-008)

**Performance Constraints**:
- Pod startup < 30 seconds (SC-009)
- Deployment completion < 10 minutes (SC-001, SC-006)
- Rolling update < 2 minutes (SC-010)

**Reliability Constraints**:
- Minimum 2 replicas (FR-011)
- All health checks must pass (SC-001)
- 100% deployment success rate (SC-003)

**Security Constraints**:
- Containers run as non-root (FR-004)
- Read-only root filesystem (FR-015)
- Secrets managed via Kubernetes Secrets (FR-045)
- No hardcoded secrets in manifests/Dockerfiles

---

## References

- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Research Findings](./research.md)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
