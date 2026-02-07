# Quick Start Guide: Local Kubernetes Deployment for Todo AI Chatbot

**Feature**: Phase IV - Local Kubernetes Deployment
**Date**: 2026-01-30
**Estimated Time**: 10-15 minutes

---

## Overview

This guide walks you through deploying the Todo AI Chatbot on a local Minikube cluster using Docker, Helm, and AI-powered DevOps tools (kubectl-ai, kagent). The entire deployment runs locally on your machine with zero cloud costs.

---

## Prerequisites

### Required Software

**1. Docker Desktop** (v4.53+)
- Download: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Verify: `docker --version`
- Start Docker Desktop before proceeding

**2. Minikube** (v1.32+)
- Download: [minikube.sigs.k8s.io/docs/start](https://minikube.sigs.k8s.io/docs/start/)
- Verify: `minikube version`
- Requires: 8GB RAM, 4 CPU cores minimum

**3. kubectl** (v1.32+)
- Download: [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/)
- Verify: `kubectl version --client`
- Note: Minikube includes kubectl, but separate installation is recommended

**4. Helm** (v3.16+)
- Download: [helm.sh/docs/intro/install](https://helm.sh/docs/intro/install/)
- Verify: `helm version`

**5. OpenAI API Key**
- Required for chatbot functionality
- Create account: [platform.openai.com](https://platform.openai.com)
- Generate API key from settings

### Optional AI DevOps Tools

**6. kubectl-ai** (AI Kubernetes assistant)
- Install: `npm install -g kubectl-ai`
- Requires: OpenAI API key (set via `kubectl-ai config set openai_api_key`)
- Verify: `kubectl-ai --version`

**7. kagent** (AI cluster analyzer)
- Install: `npm install -g kagent`
- Requires: OpenAI API key
- Verify: `kagent --version`

---

## Step 1: Start Minikube Cluster

**1. Start Minikube with Docker driver:**
```bash
minikube start --driver=docker --cpus=4 --memory=8192
```

**2. Verify cluster status:**
```bash
minikube status
```

**Expected output:**
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

**3. Enable required add-ons:**
```bash
minikube addons enable dashboard
minikube addons enable metrics-server
```

**4. Verify kubectl is configured:**
```bash
kubectl get nodes
```

**Expected output:**
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.32.0
```

---

## Step 2: Build Docker Images

**1. Navigate to project root:**
```bash
cd /path/to/Hackathone2
```

**2. Build frontend image (multi-stage):**
```bash
cd phase-3-chatbot/frontend
docker build -t todo-chatbot-frontend:v1.0.0 .
```

**3. Build backend image (multi-stage):**
```bash
cd ../backend
docker build -t todo-chatbot-backend:v1.0.0 .
```

**4. Verify images:**
```bash
docker images | grep todo-chatbot
```

**Expected output:**
```
todo-chatbot-frontend   v1.0.0   78MB   1 minute ago
todo-chatbot-backend    v1.0.0   180MB  2 minutes ago
```

**5. Load images into Minikube:**
```bash
minikube image load todo-chatbot-frontend:v1.0.0
minikube image load todo-chatbot-backend:v1.0.0
```

---

## Step 3: Create Kubernetes Secrets

**1. Create namespace:**
```bash
kubectl create namespace todo-chatbot-dev
```

**2. Create OpenAI API key secret:**
```bash
kubectl create secret generic backend-secrets \
  --from-literal=OPENAI_API_KEY=sk-your-actual-openai-key-here \
  -n todo-chatbot-dev
```

**3. Create database URL secret (replace with your Neon database URL):**
```bash
kubectl create secret generic backend-config \
  --from-literal=DATABASE_URL=postgresql://user:password@ep-cool-neon.aws.neon.tech/todo_db \
  -n todo-chatbot-dev
```

**4. Verify secrets:**
```bash
kubectl get secrets -n todo-chatbot-dev
```

---

## Step 4: Deploy with Helm (Manual Method)

**1. Navigate to Helm chart:**
```bash
cd phase-4-k8s/helm
```

**2. Install Helm chart:**
```bash
helm install todo-chatbot . \
  --namespace todo-chatbot-dev \
  --values values-dev.yaml \
  --set frontend.image.repository=todo-chatbot-frontend \
  --set frontend.image.tag=v1.0.0 \
  --set backend.image.repository=todo-chatbot-backend \
  --set backend.image.tag=v1.0.0
```

**3. Verify deployment:**
```bash
helm status todo-chatbot -n todo-chatbot-dev
```

**4. Watch pods starting:**
```bash
kubectl get pods -n todo-chatbot-dev -w
```

**Expected output (after ~30 seconds):**
```
NAME                        READY   STATUS    RESTARTS   AGE
frontend-7d9f8d5c-k4m2x     1/1     Running   0          1m
backend-7c8e9e6d-j5n3y      1/1     Running   0          1m
```

---

## Step 5: Deploy with kubectl-ai (AI Method)

**Alternative: Use AI agent for deployment:**

**1. Deploy frontend with kubectl-ai:**
```bash
kubectl-ai deploy the todo chatbot frontend with 2 replicas using image todo-chatbot-frontend:v1.0.0
```

**2. Deploy backend with kubectl-ai:**
```bash
kubectl-ai deploy the todo chatbot backend with 2 replicas using image todo-chatbot-backend:v1.0.0
```

**3. Create LoadBalancer service with kubectl-ai:**
```bash
kubectl-ai create a LoadBalancer service for the frontend on port 3000
```

**4. Verify deployment:**
```bash
kubectl get all -n todo-chatbot-dev
```

---

## Step 6: Access Application

**1. Start Minikube tunnel (in separate terminal):**
```bash
minikube tunnel
```

**Note**: Keep this terminal open. Press Ctrl+C to stop tunnel when done.

**2. Get LoadBalancer IP:**
```bash
kubectl get svc frontend-service -n todo-chatbot-dev
```

**Expected output:**
```
NAME              TYPE           EXTERNAL-IP     PORT(S)          AGE
frontend-service  LoadBalancer   127.0.0.1       3000:31234/TCP   5m
```

**3. Access application in browser:**
```
http://127.0.0.1:3000
```

**4. Test chatbot:**
- Type: "Add a todo to buy groceries"
- Type: "Show my todos"
- Type: "Mark the first todo as completed"

---

## Step 7: Verify Deployment

**1. Check pod status:**
```bash
kubectl get pods -n todo-chatbot-dev
```

**All pods should be Running with 1/1 READY.**

**2. Check health endpoints:**
```bash
# Frontend health
kubectl exec -n todo-chatbot-dev frontend-xxx -- curl -s http://localhost:3000/health

# Backend health (port-forward required)
kubectl port-forward -n todo-chatbot-dev backend-xxx 8000:8000
curl http://localhost:8000/health
```

**3. Check logs:**
```bash
# Frontend logs
kubectl logs -n todo-chatbot-dev frontend-xxx --tail=20 -f

# Backend logs
kubectl logs -n todo-chatbot-dev backend-xxx --tail=20 -f
```

**4. Run smoke tests:**
```bash
cd phase-4-k8s/scripts
./test-deployment.sh
```

---

## Step 8: Scale with kubectl-ai (AI Method)

**1. Scale backend to 3 replicas:**
```bash
kubectl-ai scale the backend deployment to 3 replicas
```

**2. Verify scaling:**
```bash
kubectl get pods -n todo-chatbot-dev -l app=backend
```

**Expected output:**
```
NAME                      READY   STATUS    RESTARTS   AGE
backend-7c8e9e6d-j5n3y    1/1     Running   0          10m
backend-7c8e9e6d-k5p9q    1/1     Running   0          1m
backend-7c8e9e6d-m8l2x    1/1     Running   0          1m
```

**3. Scale manually with kubectl (fallback):**
```bash
kubectl scale deployment backend --replicas=2 -n todo-chatbot-dev
```

---

## Step 9: Analyze Cluster with kagent (AI Method)

**1. Analyze cluster health:**
```bash
kagent analyze cluster health in namespace todo-chatbot-dev
```

**2. Check resource utilization:**
```bash
kagent check CPU and memory usage for all pods
```

**3. Get optimization suggestions:**
```bash
kagent suggest optimizations for resource usage
```

**4. Check resource usage manually (fallback):**
```bash
# Pod resource usage
kubectl top pods -n todo-chatbot-dev

# Node resource usage
kubectl top nodes
```

---

## Step 10: Test Rolling Update

**1. Update image tag:**
```bash
helm upgrade todo-chatbot ./helm \
  --namespace todo-chatbot-dev \
  --values values-dev.yaml \
  --set frontend.image.tag=v1.0.1 \
  --set backend.image.tag=v1.0.1 \
  --wait
```

**2. Watch rolling update:**
```bash
kubectl rollout status deployment/frontend -n todo-chatbot-dev
kubectl rollout status deployment/backend -n todo-chatbot-dev
```

**3. Verify no service interruption:**
```bash
# Terminal 1: Watch pods
kubectl get pods -n todo-chatbot-dev -w

# Terminal 2: Continuous health check
while true; do curl -s http://127.0.0.1:3000/health | jq .; sleep 2; done
```

---

## Step 11: Rollback if Needed

**1. List Helm revisions:**
```bash
helm history todo-chatbot -n todo-chatbot-dev
```

**2. Rollback to previous version:**
```bash
helm rollback todo-chatbot 1 -n todo-chatbot-dev
```

**3. Verify rollback:**
```bash
kubectl get pods -n todo-chatbot-dev
```

**4. Verify application still works:**
```bash
curl http://127.0.0.1:3000/health
```

---

## Step 12: Teardown Deployment

**1. Uninstall Helm release:**
```bash
helm uninstall todo-chatbot -n todo-chatbot-dev
```

**2. Delete namespace:**
```bash
kubectl delete namespace todo-chatbot-dev
```

**3. Verify cleanup:**
```bash
kubectl get all -n todo-chatbot-dev
```

**Expected output:**
```
No resources found in todo-chatbot-dev namespace.
```

**4. Stop Minikube tunnel:**
```bash
# Press Ctrl+C in the terminal running minikube tunnel
```

**5. Stop Minikube (optional):**
```bash
minikube stop
```

**6. Delete Minikube cluster (complete reset):**
```bash
minikube delete
```

---

## Troubleshooting

### Issue: Pods stuck in Pending state

**Cause**: Insufficient cluster resources

**Solution**:
```bash
# Check resource usage
kubectl top nodes

# Increase Minikube resources
minikube stop
minikube start --cpus=4 --memory=8192
```

---

### Issue: Pods in CrashLoopBackOff

**Cause**: Application error or missing environment variables

**Solution**:
```bash
# Check pod logs
kubectl logs -n todo-chatbot-dev backend-xxx

# Describe pod for events
kubectl describe pod -n todo-chatbot-dev backend-xxx

# Check ConfigMaps and Secrets
kubectl get configmap -n todo-chatbot-dev
kubectl get secret -n todo-chatbot-dev

# Common fixes:
# 1. Add missing environment variables to ConfigMap
# 2. Verify Secrets are created correctly
# 3. Check DATABASE_URL and OPENAI_API_KEY are valid
```

---

### Issue: Frontend not accessible via Minikube tunnel

**Cause**: Tunnel not running or service not LoadBalancer type

**Solution**:
```bash
# Verify tunnel is running (separate terminal)
minikube tunnel

# Check service type
kubectl get svc frontend-service -n todo-chatbot-dev

# Should be LoadBalancer, if not recreate service:
kubectl delete svc frontend-service -n todo-chatbot-dev
# Apply from Helm chart again
helm upgrade todo-chatbot ./helm -n todo-chatbot-dev
```

---

### Issue: kubectl-ai generates invalid manifests

**Cause**: AI agent misunderstanding or incorrect prompt

**Solution**:
```bash
# Use more specific prompts
kubectl-ai deploy a frontend deployment with 2 replicas using image todo-chatbot-frontend:v1.0.0, expose port 3000, with resource limits cpu=200m,memory=256Mi

# Fallback to manual kubectl
kubectl create deployment frontend --image=todo-chatbot-frontend:v1.0.0 -n todo-chatbot-dev
kubectl scale deployment frontend --replicas=2 -n todo-chatbot-dev
```

---

### Issue: Port 3000 already in use

**Cause**: Another process using port 3000

**Solution**:
```bash
# Check what's using port 3000 (Windows)
netstat -ano | findstr :3000

# Kill the process (replace <PID>)
taskkill /PID <PID> /F

# Or use different port via Helm values:
helm install todo-chatbot ./helm -n todo-chatbot-dev \
  --set frontend.service.port=3001
```

---

## Development Workflow

### Rapid Iteration Cycle (< 5 minutes)

**1. Make code changes:**
```bash
cd phase-3-chatbot/frontend  # or backend
# Edit files...
```

**2. Rebuild Docker image:**
```bash
docker build -t todo-chatbot-frontend:v1.0.1 .
```

**3. Load into Minikube:**
```bash
minikube image load todo-chatbot-frontend:v1.0.1
```

**4. Upgrade Helm release:**
```bash
helm upgrade todo-chatbot ./helm \
  --namespace todo-chatbot-dev \
  --set frontend.image.tag=v1.0.1 \
  --wait
```

**5. Verify changes:**
```bash
kubectl rollout status deployment/frontend -n todo-chatbot-dev
curl http://127.0.0.1:3000
```

---

## Next Steps

1. **Customize Helm Values**: Edit `phase-4-k8s/helm/values-dev.yaml` for your configuration
2. **Enable HPA**: Set `hpa.enabled=true` for auto-scaling
3. **Deploy Production-Like**: Use `values-prod.yaml` for production-like environment
4. **Explore AI Agents**: Try more kubectl-ai and kagent commands
5. **Read Full Documentation**: See [spec.md](./spec.md) and [plan.md](./plan.md)

---

## Success Criteria

From [spec.md](./spec.md):

- ✅ All pods Running and READY (1/1)
- ✅ All health checks pass (200 OK)
- ✅ Application accessible at http://127.0.0.1:3000
- ✅ Deployment completes in under 10 minutes
- ✅ Images under size limits (Frontend <100MB, Backend <200MB)
- ✅ kubectl-ai successfully deploys and scales
- ✅ kagent provides cluster health insights

---

## References

- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Data Model](./data-model.md)
- [Service Contracts](./contracts/)
- [Research Findings](./research.md)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
