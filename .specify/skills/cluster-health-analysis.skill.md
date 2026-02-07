# Cluster Health Analysis Skill

## Description
Reusable skill for monitoring and analyzing Kubernetes cluster health. Includes checking node status, pod health, resource utilization, troubleshooting issues, and using kubectl-ai for intelligent analysis.

## When to Use
- Monitoring cluster health and performance
- Troubleshooting application issues
- Analyzing resource utilization patterns
- Investigating pod failures and crashes
- Optimizing cluster resource allocation

## Capabilities

### 1. Basic Cluster Health Checks
```bash
# Check cluster info
kubectl cluster-info

# Check cluster version
kubectl version --short

# Check node status
kubectl get nodes

# Detailed node information
kubectl describe nodes

# Check all namespaces
kubectl get all --all-namespaces

# Check cluster events
kubectl get events --sort-by='.lastTimestamp'
```

### 2. Pod Health Analysis
```bash
# Get all pods with status
kubectl get pods -A

# Get pods with wide output (shows nodes)
kubectl get pods -o wide

# Get pods with labels
kubectl get pods -l app=todo-backend

# Check pod status and age
kubectl get pods -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,AGE:.metadata.creationTimestamp

# Get restart counts
kubectl get pods -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,RESTARTS:.status.containerStatuses[0].restartCount
```

### 3. Resource Utilization Analysis
```bash
# Check pod resource usage (requires metrics-server)
kubectl top pods -A

# Check node resource usage
kubectl top nodes

# Watch resource usage in real-time
kubectl top pods -w

# Get pod resource requests and limits
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.cpu}{"\t"}{.spec.containers[*].resources.requests.memory}{"\n"}{end}'

# Get node resource allocation
kubectl describe nodes | grep -A 5 "Allocated resources"
```

### 4. Log Analysis
```bash
# Get pod logs
kubectl logs <pod-name>

# Follow logs (stream)
kubectl logs -f <pod-name>

# Get logs from previous container instance
kubectl logs <pod-name> --previous

# Get logs from multiple pods
kubectl logs -l app=todo-backend

# Get logs with timestamps
kubectl logs <pod-name> --timestamps

# Get last N lines
kubectl logs <pod-name> --tail=100

# Get logs from specific container
kubectl logs <pod-name> -c <container-name>

# Get logs from all containers in pod
kubectl logs <pod-name> --all-containers=true
```

### 5. Troubleshooting Failed Pods
```bash
# Describe pod for detailed information
kubectl describe pod <pod-name>

# Check pod events
kubectl get events --field-selector involvedObject.name=<pod-name>

# Check pod status
kubectl get pod <pod-name> -o jsonpath='{.status.phase}'

# Check pod conditions
kubectl get pod <pod-name> -o jsonpath='{.status.conditions[*].message}'

# Check why pod is pending
kubectl describe pod <pod-name> | grep -A 10 "Events:"

# Check why pod is crashing
kubectl logs <pod-name> --previous

# Check pod container states
kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[*].state}'
```

### 6. Service and Endpoint Analysis
```bash
# Get all services
kubectl get services -A

# Check service endpoints
kubectl get endpoints -A

# Check specific service endpoints
kubectl get endpoints <service-name>

# Describe service
kubectl describe service <service-name>

# Test service connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://<service-name>:<port>

# Port forward to service
kubectl port-forward service/<service-name> 8080:80
```

### 7. Network Analysis
```bash
# Check network policies
kubectl get networkpolicies -A

# Check ingress resources
kubectl get ingress -A

# Describe ingress
kubectl describe ingress <ingress-name>

# Check DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup <service-name>

# Test pod-to-pod connectivity
kubectl exec <pod-name> -- curl http://<another-pod>:<port>
```

### 8. Storage Analysis
```bash
# Check persistent volumes
kubectl get pv

# Check persistent volume claims
kubectl get pvc -A

# Check storage classes
kubectl get storageclass

# Describe PV
kubectl describe pv <pv-name>

# Check PVC status
kubectl get pvc -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,CAPACITY:.spec.resources.requests.storage

# Check attached volumes
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.volumes[*].name}{"\n"}{end}'
```

### 9. Resource Quota and Limits Analysis
```bash
# Check resource quotas
kubectl get resourcequota -A

# Check limit ranges
kubectl get limitrange -A

# Describe resource quota
kubectl describe resourcequota <quota-name> -n <namespace>

# Check namespace resource usage
kubectl describe namespace <namespace>

# Check pod resource limits
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.limits.cpu}{"\t"}{.spec.containers[*].resources.limits.memory}{"\n"}{end}'
```

### 10. Using kubectl-ai for Intelligent Analysis

#### Install kubectl-ai
```bash
# Install kubectl-ai (requires OpenAI API key)
kubectl krew install ai

# Configure OpenAI API key
export OPENAI_API_KEY="sk-..."
```

#### Common kubectl-ai Commands
```bash
# Ask kubectl-ai to analyze cluster health
kubectl ai "analyze the cluster health and identify any issues"

# Get scaling recommendations
kubectl ai "check why pods are failing and suggest fixes"

# Optimize resource allocation
kubectl ai "optimize resource allocation for the todo-backend deployment"

# Troubleshoot specific issue
kubectl ai "investigate why the todo-frontend pods are crash looping"

# Security analysis
kubectl ai "check for security vulnerabilities in the cluster configuration"

# Cost optimization
kubectl ai "analyze resource usage and suggest cost optimizations"

# Performance analysis
kubectl ai "identify performance bottlenecks in the application"
```

### 11. Advanced Diagnostics

#### Pod Debugging
```bash
# Execute into pod
kubectl exec -it <pod-name> -- /bin/sh

# Debug with ephemeral container (k8s 1.23+)
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Copy files from pod
kubectl cp <pod-name>:/path/to/file ./local-file

# Check pod environment variables
kubectl exec <pod-name> -- env

# Check pod processes
kubectl exec <pod-name> -- ps aux

# Check pod network connectivity
kubectl exec <pod-name> -- netstat -tulpn
```

#### Node Analysis
```bash
# Get node details
kubectl describe node <node-name>

# Check node conditions
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[*].type}{"\t"}{.status.conditions[*].status}{"\n"}{end}'

# Check node capacity
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.capacity.cpu}{"\t"}{.status.capacity.memory}{"\n"}{end}'

# Check node allocatable resources
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\t"}{.status.allocatable.memory}{"\n"}{end}'

# Check node events
kubectl get events --field-selector involvedObject.kind=Node
```

### 12. Health Check Scripts

#### Comprehensive Health Check
```bash
#!/bin/bash
# cluster-health-check.sh

echo "=== Cluster Health Check ==="
echo ""

echo "--- Cluster Info ---"
kubectl cluster-info
echo ""

echo "--- Node Status ---"
kubectl get nodes
echo ""

echo "--- Pod Status ---"
kubectl get pods -A | grep -E "NAME|Running|Pending|Failed"
echo ""

echo "--- Resource Usage ---"
echo "Node Usage:"
kubectl top nodes
echo ""
echo "Pod Usage:"
kubectl top pods -A | head -20
echo ""

echo "--- Failed Pods ---"
kubectl get pods -A -o jsonpath='{range .items[?(@.status.phase=="Failed")]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'
echo ""

echo "--- Recent Events ---"
kubectl get events --sort-by='.lastTimestamp' | tail -20
echo ""

echo "--- Service Endpoints ---"
kubectl get endpoints -A | grep "<none>"
echo ""

echo "--- Persistent Volumes ---"
kubectl get pv | grep -E "NAME|Failed|Released"
echo ""
```

#### Resource Exhaustion Check
```bash
#!/bin/bash
# resource-check.sh

echo "=== Resource Exhaustion Check ==="
echo ""

echo "--- High CPU Usage (>80%) ---"
kubectl top pods -A --no-headers | awk '$3+0 > 80 {print $1, $2, $3}'
echo ""

echo "--- High Memory Usage (>80%) ---"
kubectl top pods -A --no-headers | awk '$4+0 > 80 {print $1, $2, $4}'
echo ""

echo "--- Pending Pods (resource limits?) ---"
kubectl get pods -A -o jsonpath='{range .items[?(@.status.phase=="Pending")]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'
echo ""

echo "--- Nodes with pressure ---"
kubectl get nodes -o jsonpath='{range .items[?(@.status.conditions[*].type=="MemoryPressure")]}{.metadata.name}{"\n"}{end}'
echo ""
```

### 13. Common Issues and Solutions

#### Image Pull Back Off
```bash
# Check image name and tag
kubectl describe pod <pod-name> | grep Image

# Check image pull secret
kubectl get secrets

# Check if image exists
docker pull <image-name>

# Solution: Check registry credentials and image availability
```

#### CrashLoopBackOff
```bash
# Check logs
kubectl logs <pod-name> --previous

# Check pod events
kubectl describe pod <pod-name>

# Common causes:
# - Application error
# - Missing environment variables
# - Failed health checks
# - Resource constraints
```

#### Pending Pods
```bash
# Check pod events
kubectl describe pod <pod-name> | grep Events

# Common causes:
# - Insufficient resources
# - Node selector not matching
# - Taints and tolerations
# - PVC not bound

# Solution: Check resources, node selectors, and PVCs
```

#### Resource Limits Issues
```bash
# Check pod resource limits
kubectl describe pod <pod-name> | grep -A 5 Limits

# Check OOMKilled events
kubectl get events -A | grep OOMKilled

# Solution: Increase memory limits
kubectl set resources deployment <deployment-name> --limits=memory=1Gi
```

## Best Practices

### 1. Regular Health Checks
```bash
# Set up cron job for regular checks
crontab -e

# Add: Check cluster health every hour
0 * * * * /path/to/cluster-health-check.sh >> /var/log/cluster-health.log
```

### 2. Monitor Key Metrics
```bash
# Track these metrics regularly:
# - Pod restart counts
# - Pod status (Running/Pending/Failed)
# - Resource utilization (CPU/Memory)
# - Node health
# - Recent events
```

### 3. Set Up Alerts
```yaml
# Example: Prometheus alerts
groups:
- name: cluster-health
  rules:
  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[1h]) > 0
    annotations:
      summary: "Pod {{ $labels.pod }} is crash looping"

  - alert: NodeMemoryPressure
    expr: kube_node_status_condition{condition="MemoryPressure", status!="false"} == 1
    annotations:
      summary: "Node {{ $labels.node }} has memory pressure"
```

### 4. Use kubectl-ai for Complex Issues
```bash
# When you're stuck, let kubectl-ai analyze
kubectl ai "analyze why the cluster is slow"

# Get intelligent suggestions
kubectl ai "suggest optimizations for the todo-app deployment"
```

### 5. Document Findings
```bash
# Create incident reports
kubectl get events --sort-by='.lastTimestamp' > incident-$(date +%Y%m%d).log
kubectl describe pods > pods-$(date +%Y%m%d).log
kubectl top pods -A > resources-$(date +%Y%m%d).log
```

## Dependencies
- kubectl CLI tool
- metrics-server installed on cluster (for `kubectl top` commands)
- kubectl-ai plugin (optional, for intelligent analysis)
- OpenAI API key (for kubectl-ai)
- Basic understanding of Kubernetes architecture

## Integration with kubectl-ai
- Intelligent troubleshooting and analysis
- Natural language queries about cluster state
- Automated optimization suggestions
- Security vulnerability scanning
- Performance bottleneck identification
