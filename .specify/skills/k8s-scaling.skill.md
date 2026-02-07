# Kubernetes Scaling Skill

## Description
Reusable skill for scaling Kubernetes deployments horizontally and vertically. Includes manual scaling, Horizontal Pod Autoscaler (HPA), Vertical Pod Autoscaler (VPA), and scaling strategies for different workload types.

## When to Use
- Applications need to handle increased traffic/load
- Implementing auto-scaling based on CPU/memory metrics
- Optimizing resource allocation
- Scaling deployments up or down manually
- Setting up cost-effective scaling strategies

## Capabilities

### 1. Manual Scaling
```bash
# Scale deployment to specific replica count
kubectl scale deployment/todo-backend --replicas=5

# Scale multiple deployments
kubectl scale deployment/todo-backend deployment/todo-frontend --replicas=3

# Check replica count
kubectl get deployment todo-backend

# Watch pods being created/terminated
kubectl get pods -w
```

### 2. Horizontal Pod Autoscaler (HPA)

#### CPU-Based Autoscaling
```yaml
# hpa-cpu.yaml
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
```

#### Memory-Based Autoscaling
```yaml
# hpa-memory.yaml
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
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### Custom Metrics Autoscaling
```yaml
# hpa-custom.yaml
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
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

#### Multiple Metrics Autoscaling
```yaml
# hpa-multiple.yaml
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

**Apply HPA:**
```bash
# Create HPA from YAML
kubectl apply -f hpa-cpu.yaml

# Create HPA with kubectl
kubectl autoscale deployment todo-backend \
  --min=2 --max=10 \
  --cpu-percent=70

# Check HPA status
kubectl get hpa

# Watch HPA in real-time
kubectl get hpa -w

# Describe HPA details
kubectl describe hpa todo-backend-hpa
```

### 3. Vertical Pod Autoscaler (VPA)

#### VPA for Resource Recommendations
```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: todo-backend-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  updatePolicy:
    updateMode: "Off"  # Options: Off, Initial, Recreate, Auto
  resourcePolicy:
    containerPolicies:
    - containerName: backend
      minAllowed:
        cpu: "100m"
        memory: "128Mi"
      maxAllowed:
        cpu: "1000m"
        memory: "1Gi"
      controlledResources: ["cpu", "memory"]
```

**Apply VPA:**
```bash
# Create VPA
kubectl apply -f vpa.yaml

# Check VPA recommendations
kubectl describe vpa todo-backend-vpa

# View recommended resources
kubectl get vpa todo-backend-vpa -o yaml
```

### 4. Cluster Autoscaler

#### For Minikube (Testing)
```bash
# Enable autoscaler in Minikube
minikube start --extra-config=controller-manager.cluster-signing-cert-file="/var/lib/minikube/certs/ca.crt"

# Simulate cluster scaling
minikube addons enable autoscaler
```

#### For Cloud Providers (DOKS, GKE, AKS)
```yaml
# For DigitalOcean Kubernetes
kubectl edit configmap -n kube-system cluster-autoscaler

# Add configuration
data:
  cluster-autoscaler: |
    --balance-similar-node-groups=true
    --expander=priority
    --max-nodes-total=100
    --nodes=1:10:default-node-group
```

### 5. Scaling Strategies

#### Scale Up Strategies
```yaml
behavior:
  scaleUp:
    stabilizationWindowSeconds: 0  # Immediate scale-up
    policies:
    - type: Percent
      value: 100  # Double replicas
      periodSeconds: 15
    - type: Pods
      value: 5    # Add 5 pods
      periodSeconds: 15
    selectPolicy: Max  # Use policy that creates most pods
```

#### Scale Down Strategies
```yaml
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300  # Wait 5 min before scale-down
    policies:
    - type: Percent
      value: 50  # Reduce by 50%
      periodSeconds: 15
    - type: Pods
      value: 2    # Remove 2 pods
      periodSeconds: 15
    selectPolicy: Min  # Use policy that removes fewest pods
```

### 6. Predictive Scaling (Advanced)

#### CronHPA for Scheduled Scaling
```yaml
# cronhpa.yaml
apiVersion: autoscaling.alibabacloud.com/v1beta1
kind: CronHorizontalPodAutoscaler
metadata:
  name: todo-backend-cronhpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  jobs:
  - name: "scale-up-during-business-hours"
    schedule: "0 9 * * 1-5"  # 9 AM Mon-Fri
    targetSize: 10
  - name: "scale-down-after-hours"
    schedule: "0 18 * * 1-5"  # 6 PM Mon-Fri
    targetSize: 2
  - name: "scale-down-weekends"
    schedule: "0 0 * * 6,0"   # Midnight Sat/Sun
    targetSize: 1
```

### 7. Monitoring Scaling Events

#### View HPA Events
```bash
# Get HPA events
kubectl describe hpa todo-backend-hpa | grep -A 20 Events

# Watch scaling events
kubectl get events --field-selector involvedObject.kind=HorizontalPodAutoscaler

# View specific HPA conditions
kubectl get hpa todo-backend-hpa -o jsonpath='{.status.conditions}'
```

#### Check Replica Count Changes
```bash
# View current replica count
kubectl get deployment todo-backend

# View replica count history
kubectl describe deployment todo-backend | grep -A 10 "Replica"

# Watch pods being created/terminated
kubectl get pods -l app=todo-backend -w
```

## Scaling Patterns

### 1. Predictable Workload (Static Scaling)
```yaml
# Fixed replicas for known traffic patterns
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
spec:
  replicas: 5  # Known steady-state load
```

### 2. Variable Workload (HPA)
```yaml
# Autoscale based on metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
spec:
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 3. Burst Workload (Provisional Scaling)
```yaml
behavior:
  scaleUp:
    policies:
    - type: Pods
      value: 10  # Add 10 pods immediately
      periodSeconds: 10
```

### 4. Cost-Optimized Scaling
```yaml
# Aggressive scale-down
behavior:
  scaleDown:
    stabilizationWindowSeconds: 60  # Short window
    policies:
    - type: Percent
      value: 80  # Remove 80% of pods
      periodSeconds: 15
```

## Best Practices

### 1. Set Appropriate Resource Requests
```yaml
resources:
  requests:
    cpu: "250m"      # Must be set for HPA to work
    memory: "256Mi"  # Must be set for HPA to work
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### 2. Use Multiple Metrics
```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      averageUtilization: 70
- type: Resource
  resource:
    name: memory
    target:
      averageUtilization: 80
```

### 3. Configure Scaling Behavior
```yaml
behavior:
  scaleUp:
    stabilizationWindowSeconds: 0
  scaleDown:
    stabilizationWindowSeconds: 300
```

### 4. Set Minimum and Maximum Bounds
```yaml
minReplicas: 2   # Prevent scaling to zero
maxReplicas: 10  # Control cost ceiling
```

### 5. Test Scaling Behavior
```bash
# Load test to trigger scale-up
kubectl run -it --rm load-test --image=busybox -- sh -c \
  "while true; do wget -q -O- http://todo-backend-service; done"

# Monitor HPA during test
kubectl get hpa -w

# Monitor pods during test
kubectl get pods -w
```

## Troubleshooting Scaling Issues

### HPA Not Scaling
```bash
# Check if metrics server is installed
kubectl get deployment metrics-server -n kube-system

# Install metrics server if missing
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify HPA can get metrics
kubectl describe hpa todo-backend-hpa
```

### Pods Not Scaling Down
```bash
# Check scale-down stabilization window
kubectl get hpa todo-backend-hpa -o yaml | grep -A 10 behavior

# Check if pods are near resource limits
kubectl top pods -l app=todo-backend

# View HPA conditions
kubectl describe hpa todo-backend-hpa | grep -A 10 Conditions
```

### Excessive Scaling
```bash
# Check current replica count
kubectl get deployment todo-backend

# Adjust HPA parameters
kubectl edit hpa todo-backend-hpa

# Set tighter scale-up policies
kubectl patch hpa todo-backend-hpa -p '{"spec":{"behavior":{"scaleUp":{"stabilizationWindowSeconds":60}}}}'
```

## Performance Metrics

### Monitor Resource Utilization
```bash
# Get pod resource usage
kubectl top pods -l app=todo-backend

# Get node resource usage
kubectl top nodes

# Watch resource usage in real-time
kubectl top pods -l app=todo-backend -w
```

### Analyze Scaling Events
```bash
# Get HPA metrics
kubectl get hpa todo-backend-hpa -o jsonpath='{.status.currentMetrics}'

# View scaling events
kubectl get events --field-selector reason=TriggeredScaleUp

# Check HPA recommendations
kubectl describe hpa todo-backend-hpa
```

## Cost Optimization

### Right-Size Resources
```yaml
# Start with small requests
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"

# Let VPA recommend optimal values
# Apply recommendations from VPA describe output
resources:
  requests:
    cpu: "250m"      # VPA recommended
    memory: "256Mi"  # VPA recommended
```

### Use Cluster Autoscaler
```yaml
# Scale cluster nodes based on pod demand
# Only pay for nodes you need
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler
  namespace: kube-system
data:
  cluster-autoscaler: |
    --scale-down-unneeded-time=10m
    --max-nodes-total=20
    --nodes=2:20:default-node-group
```

## Dependencies
- Kubernetes cluster with Metrics Server installed
- kubectl CLI tool
- Deployments with resource requests configured
- Sufficient cluster capacity for max replicas

## Integration with Cloud Providers
- **DOKS**: Cluster autoscaler available
- **GKE**: HPA, VPA, and cluster autoscaler fully supported
- **AKS**: HPA, VPA, and cluster autoscaler fully supported
- **Minikube**: HPA works for testing (limited cluster autoscaling)
