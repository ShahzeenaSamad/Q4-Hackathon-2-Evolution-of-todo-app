# Health Check Contracts

**Purpose**: Define health check endpoints and probe configurations for all services
**Version**: 1.0.0
**Date**: 2026-01-30

---

## Overview

This document defines the health check contracts for the Todo AI Chatbot services. Health checks are critical for Kubernetes self-healing, rolling deployments, and service mesh integration.

---

## Frontend Health Checks

### /health (Liveness)

**Endpoint**: `GET /health`
**Port**: 3000
**Path**: `/health`

**Request**:
```http
GET /health HTTP/1.1
Host: frontend-service
User-Agent: kube-probe/1.0
```

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T12:00:00Z",
  "uptime": 3600
}
```

**Failure Response** (503 Service Unavailable):
```json
{
  "status": "unhealthy",
  "error": "Service not responding"
}
```

**Purpose**: Determine if the frontend container is alive

**Kubernetes Probe Configuration**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
    scheme: HTTP
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

**Behavior**:
- **3 consecutive failures** → Pod is restarted
- **1 success** → Pod is considered alive
- Checks every **10 seconds** after **10 second** initial delay

---

### /ready (Readiness)

**Endpoint**: `GET /ready`
**Port**: 3000
**Path**: `/ready`

**Request**:
```http
GET /ready HTTP/1.1
Host: frontend-service
User-Agent: kube-probe/1.0
```

**Success Response** (200 OK):
```json
{
  "status": "ready",
  "timestamp": "2026-01-30T12:00:00Z",
  "dependencies": {
    "backend": "healthy",
    "backend_url": "http://backend-service:8000"
  }
}
```

**Failure Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "timestamp": "2026-01-30T12:00:00Z",
  "dependencies": {
    "backend": "unreachable",
    "error": "Connection refused to backend-service:8000"
  }
}
```

**Purpose**: Determine if the frontend container is ready to serve traffic

**Kubernetes Probe Configuration**:
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 3000
    scheme: HTTP
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

**Behavior**:
- **3 consecutive failures** → Pod is removed from Service load balancer
- **1 success** → Pod is added to Service load balancer
- Checks every **10 seconds** after **10 second** initial delay

---

## Backend Health Checks

### /health (Liveness)

**Endpoint**: `GET /health`
**Port**: 8000
**Path**: `/health`

**Request**:
```http
GET /health HTTP/1.1
Host: backend-service
User-Agent: kube-probe/1.0
```

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T12:00:00Z",
  "uptime": 3600,
  "database": "connected",
  "database_pool": {
    "active": 2,
    "idle": 8,
    "max_size": 10
  }
}
```

**Failure Response** (503 Service Unavailable):
```json
{
  "status": "unhealthy",
  "error": "Database connection lost"
}
```

**Purpose**: Determine if the backend container is alive

**Kubernetes Probe Configuration**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
    scheme: HTTP
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

**Behavior**:
- **3 consecutive failures** → Pod is restarted
- **1 success** → Pod is considered alive
- Checks every **10 seconds** after **10 second** initial delay

---

### /ready (Readiness)

**Endpoint**: `GET /ready`
**Port**: 8000
**Path**: `/ready`

**Request**:
```http
GET /ready HTTP/1.1
Host: backend-service
User-Agent: kube-probe/1.0
```

**Success Response** (200 OK):
```json
{
  "status": "ready",
  "timestamp": "2026-01-30T12:00:00Z",
  "dependencies": {
    "database": "connected",
    "openai": "authenticated"
  }
}
```

**Failure Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "timestamp": "2026-01-30T12:00:00Z",
  "dependencies": {
    "database": "disconnected",
    "openai": "authenticated"
  },
  "errors": [
    "Failed to connect to database: Connection timeout"
  ]
}
```

**Purpose**: Determine if the backend container is ready to serve traffic

**Kubernetes Probe Configuration**:
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
    scheme: HTTP
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

**Behavior**:
- **3 consecutive failures** → Pod is removed from Service load balancer
- **1 success** → Pod is added to Service load balancer
- Checks every **10 seconds** after **10 second** initial delay

---

## Startup Probes

### Frontend Startup Probe

**Kubernetes Probe Configuration**:
```yaml
startupProbe:
  httpGet:
    path: /health
    port: 3000
    scheme: HTTP
  initialDelaySeconds: 0
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3  # 30 seconds total (10s * 3)
```

**Purpose**: Give the container time to start before failing liveness/readiness checks

**Behavior**:
- **3 consecutive failures** → Pod is restarted (container failed to start in 30s)
- **1 success** → Startup probe disabled, liveness/readiness take over
- Checks every **10 seconds** with **no initial delay**

---

### Backend Startup Probe

**Kubernetes Probe Configuration**:
```yaml
startupProbe:
  httpGet:
    path: /health
    port: 8000
    scheme: HTTP
  initialDelaySeconds: 0
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3  # 30 seconds total (10s * 3)
```

**Purpose**: Give the container time to start (including database connection) before failing liveness/readiness checks

**Behavior**:
- **3 consecutive failures** → Pod is restarted (container failed to start in 30s)
- **1 success** → Startup probe disabled, liveness/readiness take over
- Checks every **10 seconds** with **no initial delay**

---

## Probe Configuration Summary

| Probe Type | Frontend Endpoint | Backend Endpoint | Initial Delay | Period | Timeout | Failure Threshold |
|------------|-------------------|------------------|---------------|--------|---------|-------------------|
| **Liveness** | /health:3000 | /health:8000 | 10s | 10s | 5s | 3 |
| **Readiness** | /ready:3000 | /ready:8000 | 10s | 10s | 5s | 3 |
| **Startup** | /health:3000 | /health:8000 | 0s | 10s | 5s | 3 |

---

## Health Check Implementation Requirements

### Frontend (Next.js)

**File**: `frontend/app/api/health/route.ts` (App Router) or `frontend/pages/api/health.ts` (Pages Router)

```typescript
export async function GET() {
  return Response.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
}
```

**File**: `frontend/app/api/ready/route.ts`

```typescript
export async function GET() {
  // Check backend connectivity
  const backendHealthy = await checkBackendHealth();

  if (!backendHealthy) {
    return Response.json({
      status: 'not_ready',
      dependencies: {
        backend: 'unreachable'
      }
    }, { status: 503 });
  }

  return Response.json({
    status: 'ready',
    dependencies: {
      backend: 'healthy'
    }
  });
}
```

---

### Backend (FastAPI)

**File**: `backend/main.py`

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/health")
async def health_check():
    """Liveness probe - check if service is alive"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": time.time() - start_time,
        "database": "connected"
    }

@app.get("/ready")
async def readiness_check():
    """Readiness probe - check if service is ready to serve traffic"""
    # Check database connection
    db_healthy = await check_database()
    openai_healthy = await check_openai()

    dependencies = {
        "database": "connected" if db_healthy else "disconnected",
        "openai": "authenticated" if openai_healthy else "unauthenticated"
    }

    if not all([db_healthy, openai_healthy]):
        return {
            "status": "not_ready",
            "dependencies": dependencies
        }, 503

    return {
        "status": "ready",
        "dependencies": dependencies
    }
```

---

## Health Check Failure Scenarios

### Scenario 1: Frontend Pod CrashLoopBackOff

**Symptoms**:
- Pod status: `CrashLoopBackOff`
- Restart count: Increasing

**Diagnosis**:
```bash
kubectl describe pod frontend-xxx -n todo-chatbot-dev
kubectl logs frontend-xxx -n todo-chatbot-dev --previous
```

**Common Causes**:
1. Application error on startup (check logs)
2. Missing environment variables (check ConfigMap)
3. Port conflict (check service configuration)
4. Image pull failure (check image name/tag)

**Resolution**:
- Fix application code
- Add missing environment variables to ConfigMap
- Verify port configuration matches EXPOSE in Dockerfile
- Check image exists: `docker images | grep todo-chatbot-frontend`

---

### Scenario 2: Backend Not Ready

**Symptoms**:
- Pod status: `Running` but not `Ready`
- Readiness probe failing

**Diagnosis**:
```bash
kubectl describe pod backend-xxx -n todo-chatbot-dev
kubectl logs backend-xxx -n todo-chatbot-dev
```

**Common Causes**:
1. Database connection failed (check DATABASE_URL)
2. OpenAI API key invalid (check OPENAI_API_KEY)
3. Database schema not created (run migrations)
4. Backend service not accessible from frontend (check network policies)

**Resolution**:
- Verify DATABASE_URL in Secret or ConfigMap
- Verify OPENAI_API_KEY in Secret
- Run database migrations
- Check network policies allow frontend → backend communication

---

### Scenario 3: All Pods Restarting

**Symptoms**:
- All pods restarting repeatedly
- Cluster-wide health check failures

**Diagnosis**:
```bash
kubectl get pods -n todo-chatbot-dev
kubectl get events -n todo-chatbot-dev --sort-by='.lastTimestamp'
minikube status
```

**Common Causes**:
1. Minikube out of resources (CPU/memory)
2. Node not ready (check Minikube status)
3. Network plugin not working (check CNI)
4. Corrupted Docker images

**Resolution**:
- Increase Minikube resources: `minikube start --cpus=4 --memory=8192`
- Restart Minikube: `minikube delete && minikube start`
- Check Docker Desktop is running
- Rebuild Docker images

---

## Monitoring Health Checks

### Manual Health Check

```bash
# Frontend health
kubectl exec -n todo-chatbot-dev frontend-xxx -- curl -s http://localhost:3000/health

# Backend health (via port-forward)
kubectl port-forward -n todo-chatbot-dev backend-xxx 8000:8000
curl http://localhost:8000/health

# Service endpoints
kubectl get endpoints -n todo-chatbot-dev
```

---

### Automated Health Check

```bash
# Watch pod status
watch kubectl get pods -n todo-chatbot-dev

# Check probe failures
kubectl describe pod frontend-xxx -n todo-chatbot-dev | grep -A 5 "Liveness"

# Check events
kubectl get events -n todo-chatbot-dev --field-selector reason=Unhealthy
```

---

## Success Criteria

From [spec.md](./spec.md#success-criteria):

- **SC-001**: All pods Running AND all health checks pass AND application accessible (within 10 min)
- **SC-009**: All pods pass health checks within 30 seconds of deployment
- **FR-013**: All pods MUST have liveness and readiness probes defined
- **FR-042**: Health checks MUST validate both frontend and backend are operational

---

## References

- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Frontend Service Contract](./frontend-api.md)
- [Backend Service Contract](./backend-api.md)
- [Feature Specification](./spec.md)
