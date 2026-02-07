# Kubernetes Deployment Skill

## Description
Reusable skill for deploying containerized applications to Kubernetes clusters. Includes creating deployments, services, configmaps, secrets, and managing application lifecycle.

## When to Use
- Deploying applications to Minikube (local)
- Deploying to cloud Kubernetes (DOKS, GKE, AKS)
- Managing application lifecycle in Kubernetes
- Configuring environment-specific deployments
- Implementing rolling updates and rollbacks

## Capabilities

### 1. Create Kubernetes Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  labels:
    app: todo-backend
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
        version: v1
    spec:
      containers:
      - name: backend
        image: todo-backend:v1.0.0
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Deploy to cluster:**
```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Check deployment status
kubectl get deployments
kubectl describe deployment todo-backend

# View pods
kubectl get pods -l app=todo-backend
```

### 2. Create Service (LoadBalancer/ClusterIP)
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-service
spec:
  type: LoadBalancer
  selector:
    app: todo-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
    name: http
  sessionAffinity: ClientIP
```

**Deploy service:**
```bash
# Apply service
kubectl apply -f service.yaml

# Get service URL
kubectl get services

# For Minikube
minikube service todo-backend-service --url
```

### 3. Create ConfigMap for Configuration
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  API_TIMEOUT: "30"
  MAX_CONNECTIONS: "100"
```

**Use in deployment:**
```yaml
spec:
  containers:
  - name: backend
    envFrom:
    - configMapRef:
        name: todo-config
```

### 4. Create Secret for Sensitive Data
```bash
# Create secret from literal
kubectl create secret generic todo-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=openai-api-key='sk-...'

# Create secret from file
kubectl create secret generic todo-secrets \
  --from-env-file=.env

# Create secret from YAML
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
type: Opaque
data:
  database-url: cG9zdGdyZXNxbDovLi4u  # base64 encoded
  openai-api-key: c2stLi4u  # base64 encoded
```

### 5. Complete Application Deployment
```yaml
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:v1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://todo-backend-service"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend-service
spec:
  type: LoadBalancer
  selector:
    app: todo-frontend
  ports:
  - port: 80
    targetPort: 3000
```

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: backend
        image: todo-backend:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-service
spec:
  type: ClusterIP
  selector:
    app: todo-backend
  ports:
  - port: 8000
    targetPort: 8000
```

### 6. Deploy to Minikube
```bash
# Start Minikube
minikube start

# Set docker environment to Minikube
eval $(minikube docker-env)

# Build images in Minikube context
docker build -t todo-frontend:local ./frontend
docker build -t todo-backend:local ./backend

# Apply Kubernetes manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml

# Get service URLs
minikube service todo-frontend-service --url
minikube service todo-backend-service --url

# Open in browser
minikube service todo-frontend-service
```

### 7. Rolling Updates
```bash
# Update image
kubectl set image deployment/todo-backend \
  backend=todo-backend:v1.1.0

# Watch rollout status
kubectl rollout status deployment/todo-backend

# Check rollout history
kubectl rollout history deployment/todo-backend

# Rollback to previous version
kubectl rollout undo deployment/todo-backend

# Rollback to specific revision
kubectl rollout undo deployment/todo-backend --to-revision=2
```

## Deployment Strategies

### 1. Recreate (Simple, downtime)
```yaml
spec:
  strategy:
    type: Recreate
```

### 2. RollingUpdate (Default, zero downtime)
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max pods above desired
      maxUnavailable: 0  # Max pods down during update
```

### 3. Blue-Green (Two deployments)
```bash
# Deploy new version (blue)
kubectl apply -f deployment-blue.yaml

# Test blue deployment
kubectl port-forward service/todo-backend-blue 8080:80

# Switch service to blue
kubectl patch service todo-backend-service \
  -p '{"spec":{"selector":{"version":"blue"}}}'

# Remove old green deployment
kubectl delete deployment todo-backend-green
```

## Health Checks and Probes

### Liveness Probe (Is the container running?)
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Readiness Probe (Is the container ready?)
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

### Startup Probe (Slow-starting containers)
```yaml
startupProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 0
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 30  # Allow up to 150 seconds (30 * 5)
```

## Resource Management

### Set Resource Requests and Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Horizontal Pod Autoscaler
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Apply HPA:**
```bash
kubectl apply -f hpa.yaml

# Check HPA status
kubectl get hpa

# Describe HPA
kubectl describe hpa todo-backend-hpa
```

## Configuration Management

### Environment-Specific ConfigMaps
```bash
# Development
kubectl create configmap todo-config-dev \
  --from-env-file=config/dev.env

# Production
kubectl create configmap todo-config-prod \
  --from-env-file=config/prod.env

# Use in deployment
kubectl apply -f deployment-dev.yaml
kubectl apply -f deployment-prod.yaml
```

### Immutable Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets-v1
immutable: true  # Cannot be updated after creation
type: Opaque
data:
  database-url: ...
```

## Best Practices

### 1. Use Labels and Selectors
```yaml
metadata:
  labels:
    app: todo-backend
    version: v1
    environment: production
spec:
  selector:
    matchLabels:
      app: todo-backend
```

### 2. Set Resource Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### 3. Use Liveness and Readiness Probes
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
```

### 4. Never Hardcode Secrets
```yaml
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: todo-secrets
      key: database-url
```

### 5. Use ConfigMaps for Configuration
```yaml
envFrom:
- configMapRef:
    name: todo-config
```

## Troubleshooting

### Check Pod Status
```bash
# List pods
kubectl get pods

# Describe pod
kubectl describe pod todo-backend-xxxxx

# View pod logs
kubectl logs todo-backend-xxxxx

# Follow logs
kubectl logs -f todo-backend-xxxxx

# Logs from previous container instance
kubectl logs todo-backend-xxxxx --previous
```

### Debug Common Issues
```bash
# Pods not starting
kubectl describe pod <pod-name>  # Check events

# CrashLoopBackOff
kubectl logs <pod-name>           # Check application logs

# Image pull errors
kubectl describe pod <pod-name>   # Check image name and registry access

# Service not reachable
kubectl get endpoints <service-name>  # Check if pods are selected
kubectl port-forward <pod-name> 8080:8000  # Test direct access
```

### Common Commands
```bash
# Get all resources
kubectl get all

# Get resources in namespace
kubectl get all -n todo-app

# Delete deployment
kubectl delete deployment todo-backend

# Delete all resources in file
kubectl delete -f deployment.yaml

# Apply with dry-run
kubectl apply -f deployment.yaml --dry-run=client
```

## Error Handling

### Image Pull Errors
```yaml
# Create image pull secret for private registry
kubectl create secret docker-registry regcred \
  --docker-server=ghcr.io \
  --docker-username=USERNAME \
  --docker-password=PASSWORD

# Use in deployment
spec:
  template:
    spec:
      imagePullSecrets:
      - name: regcred
```

### Resource Exhaustion
```yaml
# Increase resource limits
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

## Dependencies
- Kubernetes cluster (Minikube, DOKS, GKE, AKS)
- kubectl CLI tool
- Container images pushed to registry
- Application health endpoints (/health, /ready)

## Integration with Minikube
- Supports local development and testing
- LoadBalancer services work with `minikube tunnel`
- Easy port forwarding with `minikube service`
- Docker images built directly in Minikube environment
