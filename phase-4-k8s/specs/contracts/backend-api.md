# Backend Service Contract

**Service**: todo-chatbot-backend
**Version**: 1.0.0
**Type**: FastAPI Application
**Date**: 2026-01-30

---

## Service Overview

The backend service is a FastAPI application providing REST API endpoints for todo management and AI chatbot functionality. It stores data in Neon PostgreSQL database and uses OpenAI API for chatbot responses.

---

## Service Endpoint

**Kubernetes Internal**:
```
http://backend-service:8000
```

**Service Type**: ClusterIP (internal only)
**Cluster IP**: Auto-assigned (e.g., 10.96.123.45)

---

## Health Check Endpoints

### Liveness Probe
```http
GET /health HTTP/1.1
Host: backend-service
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T12:00:00Z",
  "database": "connected"
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
Host: backend-service
```

**Response** (200 OK):
```json
{
  "status": "ready",
  "database": "connected",
  "openai": "authenticated"
}
```

**Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "database": "disconnected"
}
```

**Purpose**: Determines if the container is ready to serve traffic

**Configuration**:
- Interval: 10 seconds
- Timeout: 5 seconds
- Failure threshold: 3 failures → mark pod not ready

---

## Public API Endpoints

### Root
```http
GET / HTTP/1.1
```

**Response** (200 OK):
```json
{
  "message": "Todo AI Chatbot Backend API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

**Purpose**: API root endpoint with documentation link

---

### API Documentation
```http
GET /docs HTTP/1.1
```

**Response**: Interactive Swagger UI (FastAPI auto-generated)

**Purpose**: Interactive API documentation

---

### List Todos
```http
GET /todos HTTP/1.1
Authorization: Bearer {token} (optional)
```

**Response** (200 OK):
```json
{
  "todos": [
    {
      "id": "uuid-1",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-30T12:00:00Z",
      "updated_at": "2026-01-30T12:00:00Z"
    }
  ],
  "count": 1
}
```

**Purpose**: Retrieve all todos for authenticated user

---

### Create Todo
```http
POST /todos HTTP/1.1
Content-Type: application/json
Authorization: Bearer {token} (optional)

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid-2",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-30T12:00:00Z",
  "updated_at": "2026-01-30T12:00:00Z"
}
```

**Purpose**: Create a new todo

---

### Update Todo
```http
PUT /todos/{todo_id} HTTP/1.1
Content-Type: application/json
Authorization: Bearer {token} (optional)

{
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, butter",
  "completed": true
}
```

**Response** (200 OK):
```json
{
  "id": "uuid-2",
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, butter",
  "completed": true,
  "created_at": "2026-01-30T12:00:00Z",
  "updated_at": "2026-01-30T12:05:00Z"
}
```

**Purpose**: Update an existing todo

---

### Delete Todo
```http
DELETE /todos/{todo_id} HTTP/1.1
Authorization: Bearer {token} (optional)
```

**Response** (200 OK):
```json
{
  "message": "Todo deleted successfully",
  "id": "uuid-2"
}
```

**Purpose**: Delete a todo

---

### Chatbot Endpoint
```http
POST /chat HTTP/1.1
Content-Type: application/json

{
  "message": "Add a todo to buy milk",
  "context": {
    "user_id": "uuid-user"
  }
}
```

**Response** (200 OK):
```json
{
  "response": "I've added 'Buy milk' to your todo list.",
  "action": "create_todo",
  "todo": {
    "id": "uuid-3",
    "title": "Buy milk",
    "completed": false
  }
}
```

**Purpose**: Process natural language todo operations via OpenAI

---

## Environment Variables

### Required Variables

**DATABASE_URL**:
- Description: Neon PostgreSQL connection string
- Format: `postgresql://user:password@host/database`
- Source: Secret (backend-secrets) or ConfigMap
- Example: `postgresql://todo_user:pass@ep-cool-neon.aws.neon.tech/todo_db`

**OPENAI_API_KEY**:
- Description: OpenAI API key for chatbot functionality
- Format: `sk-xxxxxxxxxxxxxxxxxxxx`
- Source: Secret (backend-secrets)
- Required: Yes

**API_PORT**:
- Description: FastAPI application port
- Default: `8000`
- Source: Dockerfile CMD or ConfigMap

### Optional Variables

**LOG_LEVEL**:
- Description: Logging verbosity
- Values: `debug`, `info`, `warn`, `error`
- Default: `info`
- Source: ConfigMap (backend-config)

**CORS_ORIGINS**:
- Description: Allowed CORS origins for frontend
- Default: `http://localhost:3000,http://frontend-service:3000`
- Source: ConfigMap (backend-config)

**NEON_DB_URL** (alternative to DATABASE_URL):
- Description: Neon database connection pool URL
- Format: Same as DATABASE_URL
- Source: Secret (backend-secrets)

---

## Dependencies

### Neon Database
**Type**: PostgreSQL (managed service)
**Purpose**: Persistent todo storage
**Connection**: From backend pods via `DATABASE_URL`

**Health Check**: Database connection validated in `/health` endpoint

---

### OpenAI API
**Type**: External API
**Purpose**: AI chatbot responses for natural language processing
**Authentication**: Via `OPENAI_API_KEY` environment variable

**Health Check**: API key validated in `/ready` endpoint

---

## Container Configuration

**Image**: `todo-chatbot-backend:v1.0.0`
**Port**: 8000
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
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

---

## Helm Template Values

```yaml
backend:
  enabled: true
  image:
    repository: todo-chatbot-backend
    tag: v1.0.0
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 8000
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
    DATABASE_URL: postgresql://todo_user:pass@ep-cool-neon.aws.neon.tech/todo_db
    LOG_LEVEL: info
    API_PORT: "8000"
    CORS_ORIGINS: "http://localhost:3000,http://frontend-service:3000"

  secrets:
    OPENAI_API_KEY: sk-xxxxxxxxxxxxxxxxxxxx

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

### HTTP 400 Bad Request
**Cause**: Invalid request body or parameters

**Response**:
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "title",
      "message": "Title is required"
    }
  ]
}
```

---

### HTTP 401 Unauthorized
**Cause**: Missing or invalid authentication token

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

### HTTP 404 Not Found
**Cause**: Resource not found

**Response**:
```json
{
  "detail": "Todo not found"
}
```

---

### HTTP 500 Internal Server Error
**Cause**: Database connection failure, OpenAI API error, or unexpected error

**Response**:
```json
{
  "detail": "Internal server error",
  "error_id": "uuid-error-id"
}
```

---

### HTTP 503 Service Unavailable
**Cause**: Database connection lost or OpenAI API unreachable

**Response**:
```json
{
  "detail": "Service temporarily unavailable",
  "retry_after": 30
}
```

---

## Testing

### Smoke Test
```bash
# Wait for rollout
kubectl rollout status deployment/backend -n todo-chatbot-dev

# Check pod status
kubectl get pods -n todo-chatbot-dev -l app=backend

# Port-forward to local machine
kubectl port-forward -n todo-chatbot-dev backend-xxx 8000:8000

# Test health endpoint
curl http://localhost:8000/health

# Test todos endpoint
curl http://localhost:8000/todos

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a todo to buy milk"}'
```

---

## Database Schema

**Todos Table**:
```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_completed ON todos(completed);
```

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Neon PostgreSQL Documentation](https://neon.tech/docs)
- [Frontend Service Contract](./frontend-api.md)
- [Health Check Contracts](./health-checks.md)
