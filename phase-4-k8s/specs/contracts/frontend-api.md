# Frontend Service Contract

**Service**: todo-chatbot-frontend
**Version**: 1.0.0
**Type**: Next.js 16+ Application
**Date**: 2026-01-30

---

## Service Overview

The frontend service is a Next.js 16+ application providing the user interface for the Todo AI Chatbot. It communicates with the backend service for todo CRUD operations and AI chatbot functionality.

---

## Service Endpoint

**Local Access** (via Minikube tunnel):
```
http://127.0.0.1:3000
```

**Kubernetes Internal**:
```
http://frontend-service:3000
```

**Service Type**: LoadBalancer
**External IP**: 127.0.0.1 (provided by Minikube tunnel)

---

## Health Check Endpoints

### Liveness Probe
```http
GET /health HTTP/1.1
Host: frontend-service
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T12:00:00Z"
}
```

**Purpose**: Determines if the container is alive and needs restart

**Configuration**:
- Interval: 10 seconds
- Timeout: 5 seconds
- Failure threshold: 3 failures → restart pod

---

### Readiness Probe
```http
GET /ready HTTP/1.1
Host: frontend-service
```

**Response** (200 OK):
```json
{
  "status": "ready",
  "dependencies": {
    "backend": "healthy"
  }
}
```

**Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "dependencies": {
    "backend": "unreachable"
  }
}
```

**Purpose**: Determines if the container is ready to serve traffic

**Configuration**:
- Interval: 10 seconds
- Timeout: 5 seconds
- Failure threshold: 3 failures → mark pod not ready

---

## Public API Endpoints

### Root Page
```http
GET / HTTP/1.1
```

**Response**: HTML page (Next.js app)

**Purpose**: Main chatbot interface

---

### Static Assets
```http
GET /_next/static/* HTTP/1.1
GET /favicon.ico HTTP/1.1
```

**Response**: Static files (CSS, JS, images)

**Purpose**: Next.js static assets

---

### API Proxy (Next.js API Routes)
```http
POST /api/todos HTTP/1.1
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Purpose**: Proxy to backend API (server-side API routes)

**Backend Forwarding**:
```http
POST http://backend-service:8000/todos HTTP/1.1
```

---

## Environment Variables

### Required Variables

**NEXT_PUBLIC_API_URL**:
- Description: Backend service URL for API calls
- Default: `http://backend-service:8000`
- Source: ConfigMap (frontend-config)

**NEXT_PUBLIC_APP_NAME**:
- Description: Application name displayed in UI
- Default: `Todo AI Chatbot`
- Source: ConfigMap (frontend-config)

**NEXT_PUBLIC_ENVIRONMENT**:
- Description: Environment name (dev, staging, production)
- Default: `dev`
- Source: ConfigMap (frontend-config)

### Optional Variables

**NEXT_PUBLIC_OPENAI_KEY** (if client-side OpenAI calls):
- Description: OpenAI API key (prefer server-side, not exposed to client)
- Default: null
- Source: Secret (frontend-secrets) - NOT RECOMMENDED

**PORT**:
- Description: Container port
- Default: `3000`
- Source: Dockerfile CMD

---

## Dependencies

### Backend Service
**Service**: todo-chatbot-backend
**Internal URL**: `http://backend-service:8000`
**Purpose**: Todo CRUD operations, AI chatbot responses

**Health Check**:
```http
GET /health HTTP/1.1
Host: backend-service
```

---

## Container Configuration

**Image**: `todo-chatbot-frontend:v1.0.0`
**Port**: 3000
**Protocol**: TCP

**Resource Limits** (Production-like):
- CPU Request: 100m
- CPU Limit: 200m
- Memory Request: 128Mi
- Memory Limit: 256Mi

**Resource Limits** (Development):
- CPU Request: 50m
- CPU Limit: 100m
- Memory Request: 64Mi
- Memory Limit: 128Mi

**Security Context**:
- Run as non-root: Yes (uid 1000)
- Read-only root filesystem: Yes
- Allow privilege escalation: No

---

## Kubernetes Deployment Specification

**Replica Count**:
- Development: 1
- Production-like: 2-3 (with HPA scaling 2-10)

**Deployment Strategy**: RollingUpdate
- MaxUnavailable: 25% (1 pod)
- MaxSurge: 25% (1 pod)

**Probes**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

---

## Helm Template Values

```yaml
frontend:
  enabled: true
  image:
    repository: todo-chatbot-frontend
    tag: v1.0.0
    pullPolicy: IfNotPresent

  service:
    type: LoadBalancer
    port: 3000
    annotations: {}

  replicaCount: 2

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 200m
      memory: 256Mi

  env:
    NEXT_PUBLIC_API_URL: http://backend-service:8000
    NEXT_PUBLIC_APP_NAME: Todo AI Chatbot
    NEXT_PUBLIC_ENVIRONMENT: dev

  hpa:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80

  nodeSelector: {}
  tolerations: []
  affinity: {}
```

---

## Error Handling

### HTTP 500 Internal Server Error
**Cause**: Application error, unhandled exception

**Response**:
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

### HTTP 503 Service Unavailable
**Cause**: Backend dependency not ready

**Response**:
```json
{
  "error": "Service unavailable",
  "message": "Backend service is not ready"
}
```

---

## Testing

### Smoke Test
```bash
# Wait for rollout
kubectl rollout status deployment/frontend -n todo-chatbot-dev

# Check pod status
kubectl get pods -n todo-chatbot-dev -l app=frontend

# Check health
kubectl exec -n todo-chatbot-dev frontend-xxx -- curl -s http://localhost:3000/health

# Access via Minikube tunnel (separate terminal)
minikube tunnel

# Test from browser
curl http://127.0.0.1:3000
```

---

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Backend Service Contract](./backend-api.md)
- [Health Check Contracts](./health-checks.md)
