# Todo AI Chatbot - Local Kubernetes Deployment

**Phase IV**: Local Kubernetes Deployment for Cloud-Native Todo AI Chatbot
**Version**: 1.0.0
**Status**: MVP Ready (Phase 3 Complete)

---

## 🎯 Overview

This project enables you to deploy the Todo AI Chatbot on your local machine using Kubernetes (Minikube), Docker, and Helm. The entire deployment runs locally with zero cloud costs, demonstrating spec-driven infrastructure automation and AI-augmented DevOps workflows.

### Features

- ✅ **Local Kubernetes Deployment**: Complete chatbot running on Minikube
- ✅ **Containerized**: Multi-stage Docker builds (frontend: 80.5MB, backend: 84.2MB)
- ✅ **Helm Charts**: Easy deployment with environment-specific configurations
- ✅ **Health Monitoring**: Liveness, readiness, and startup probes
- ✅ **Auto-Scaling**: HorizontalPodAutoscaler (HPA) support
- ✅ **AI-Ready**: Integration points for kubectl-ai and kagent
- ✅ **Production-Like**: Rolling updates, resource limits, security hardening

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Docker Desktop** 4.53+ ([Download](https://www.docker.com/products/docker-desktop))
- **Minikube** 1.32+ ([Download](https://minikube.sigs.k8s.io/docs/start/))
- **kubectl** 1.32+ ([Download](https://kubernetes.io/docs/tasks/tools/))
- **Helm** 3.16+ ([Download](https://helm.sh/docs/intro/install/))
- **OpenAI API Key** ([Get here](https://platform.openai.com/api-keys))

### 1️⃣ Start Minikube

```bash
cd phase-4-k8s
./scripts/setup-minikube.sh
```

**Expected output**:
- Minikube starts with Docker driver (4 CPUs, 8GB RAM)
- Dashboard and metrics-server enabled
- Namespace `todo-chatbot-dev` created

### 2️⃣ Build Docker Images

```bash
./scripts/build-images.sh
```

**Expected output**:
- Frontend image built: `todo-chatbot-frontend:v1.0.0` (80.5MB)
- Backend image built: `todo-chatbot-backend:v1.0.0` (84.2MB)
- Images loaded into Minikube

### 3️⃣ Deploy Application

```bash
export OPENAI_API_KEY="sk-your-actual-openai-key-here"
./scripts/deploy.sh
```

**Expected output**:
- Secrets created (OPENAI_API_KEY)
- Helm chart installed
- Pods started (frontend, backend)
- Services created

### 4️⃣ Start Minikube Tunnel

**In a separate terminal**:

```bash
minikube tunnel
```

**Keep this terminal open!** This provides the LoadBalancer IP for the frontend.

### 5️⃣ Access Application

Once the tunnel is running, open your browser:

```
http://127.0.0.1:3000
```

**You should see**: Todo AI Chatbot interface

### 6️⃣ Test Deployment

```bash
./scripts/test-deployment.sh
```

**Expected output**:
- ✅ Pods are Running
- ✅ Services exist
- ✅ Frontend is healthy
- ✅ Backend is healthy

---

## 🧹 Teardown

### Stop Application (Keep Minikube)

```bash
./scripts/teardown.sh
```

**Removes**:
- Helm release
- Namespace and all resources

**Keeps**:
- Minikube cluster running
- Docker images

### Delete Everything (Including Minikube)

```bash
./scripts/teardown.sh --delete-cluster
```

**Removes**:
- Everything above
- Minikube cluster
- All Kubernetes resources

---

## 📁 Project Structure

```
phase-4-k8s/
├── specs/                    # Design documents
│   ├── spec.md              # Feature specification
│   ├── plan.md              # Implementation plan
│   ├── research.md          # Technology decisions
│   ├── data-model.md        # Kubernetes entities
│   ├── contracts/            # Service contracts
│   └── quickstart.md         # Detailed deployment guide
├── docker/                   # Dockerfiles
│   ├── frontend/Dockerfile   # Next.js multi-stage build
│   └── backend/Dockerfile    # FastAPI multi-stage build
├── helm/                     # Helm chart
│   ├── Chart.yaml            # Chart metadata
│   ├── values.yaml           # Default configuration
│   ├── values-dev.yaml       # Development overrides
│   ├── values-prod.yaml      # Production-like overrides
│   └── templates/            # Kubernetes templates
│       ├── _helpers.tpl       # Template helpers
│       ├── *-configmap.yaml  # Environment variables
│       ├── *-secret.yaml     # Secrets
│       ├── *-deployment.yaml # Deployments
│       ├── *-service.yaml    # Services
│       └── *-hpa.yaml        # Auto-scalers
├── scripts/                  # Deployment scripts
│   ├── setup-minikube.sh    # Start Minikube
│   ├── build-images.sh      # Build Docker images
│   ├── deploy.sh             # Deploy with Helm
│   ├── test-deployment.sh    # Smoke tests
│   └── teardown.sh          # Clean up
└── tasks.md                  # Implementation tasks
```

---

## 🔧 Configuration

### Environment Variables

**Frontend** (from ConfigMap):
- `NEXT_PUBLIC_API_URL`: Backend service URL
- `NEXT_PUBLIC_APP_NAME`: Application name
- `NEXT_PUBLIC_ENVIRONMENT`: Environment (dev/prod)

**Backend** (from ConfigMap):
- `DATABASE_URL`: Neon PostgreSQL connection string
- `LOG_LEVEL`: Logging verbosity (debug/info/warn/error)
- `API_PORT`: API port (default: 8000)
- `CORS_ORIGINS`: Allowed CORS origins

**Backend Secrets** (from Secret):
- `OPENAI_API_KEY`: OpenAI API key for chatbot

### Resource Limits

**Development** (values-dev.yaml):
- CPU: 50m-100m
- Memory: 64Mi-128Mi
- Replicas: 1

**Production-Like** (values-prod.yaml):
- CPU: 250m-500m
- Memory: 256Mi-512Mi
- Replicas: 3 (with HPA 2-10)

---

## 🤖 AI DevOps Integration

### kubectl-ai (AI Kubernetes Assistant)

**Install**:
```bash
npm install -g kubectl-ai
kubectl-ai config set openai_api_key $OPENAI_API_KEY
```

**Deploy with AI**:
```bash
kubectl-ai deploy the todo chatbot frontend with 2 replicas using image todo-chatbot-frontend:v1.0.0
kubectl-ai deploy the todo chatbot backend with 2 replicas using image todo-chatbot-backend:v1.0.0
```

**Scale with AI**:
```bash
kubectl-ai scale the backend deployment to 3 replicas
```

**Debug with AI**:
```bash
kubectl-ai check why the frontend pods are failing
```

### kagent (AI Cluster Analyzer)

**Install**:
```bash
npm install -g kagent
```

**Analyze Cluster Health**:
```bash
kagent analyze cluster health in namespace todo-chatbot-dev
```

**Check Resource Usage**:
```bash
kagent check CPU and memory usage for all pods
```

**Get Optimization Suggestions**:
```bash
kagent suggest optimizations for resource usage
```

---

## 📊 Health Check Endpoints

### Frontend
- **Liveness**: `GET /health` - Returns 200 OK if service is alive
- **Readiness**: `GET /ready` - Returns 200 OK if backend is reachable

### Backend
- **Liveness**: `GET /health` - Returns 200 OK with uptime
- **Readiness**: `GET /ready` - Returns 200 OK if database is connected

---

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n todo-chatbot-dev

# Describe pod for details
kubectl describe pod <pod-name> -n todo-chatbot-dev

# View pod logs
kubectl logs <pod-name> -n todo-chatbot-dev
```

### Port Already in Use

```bash
# Check what's using port 3000 (Windows)
netstat -ano | findstr :3000

# Kill the process (replace <PID>)
taskkill /PID <PID> /F
```

### Minikube Resource Issues

```bash
# Check Minikube status
minikube status

# Increase resources
minikube stop
minikube start --cpus=4 --memory=8192
```

### Database Connection Issues

```bash
# Check backend logs
kubectl logs -n todo-chatbot-dev -l app=todo-chatbot-backend

# Verify database URL in ConfigMap
kubectl get configmap -n todo-chatbot-dev
```

---

## 📚 Documentation

- **[Specification](phase-4-k8s/specs/spec.md)** - Complete feature requirements
- **[Implementation Plan](phase-4-k8s/specs/plan.md)** - Architecture and design decisions
- **[Research Findings](phase-4-k8s/specs/research.md)** - Technology decisions
- **[Data Model](phase-4-k8s/specs/data-model.md)** - Kubernetes entities
- **[Service Contracts](phase-4-k8s/specs/contracts/)** - API specifications
- **[Quick Start Guide](phase-4-k8s/specs/quickstart.md)** - Detailed deployment steps
- **[Task List](phase-4-k8s/tasks.md)** - Implementation tasks

---

## ✅ Success Criteria

- ✅ All pods Running (STATUS=Running)
- ✅ All health checks passing (200 OK)
- ✅ Application accessible at http://127.0.0.1:3000
- ✅ Deployment completes in under 10 minutes
- ✅ Frontend image <100MB compressed
- ✅ Backend image <200MB compressed
- ✅ Pods pass health checks within 30 seconds

---

## 🎉 MVP Complete!

**Phase 3 (User Story 1)** is now complete! You can deploy the Todo AI Chatbot locally on Minikube.

**Next Phases** (Optional):
- **Phase 4**: AI DevOps Integration (kubectl-ai, kagent)
- **Phase 5**: Helm Workflows (upgrade, rollback)
- **Phase 6**: Reproducibility Validation
- **Phase 7**: Polish & Optimization

---

## 📝 Development Workflow

### Rapid Iteration Cycle (< 5 minutes)

1. Make code changes
2. Rebuild image: `docker build -t todo-chatbot-frontend:v1.0.1 -f phase-4-k8s/docker/frontend/Dockerfile .`
3. Load into Minikube: `minikube image load todo-chatbot-frontend:v1.0.1`
4. Upgrade Helm: `helm upgrade todo-chatbot ./phase-4-k8s/helm --set frontend.image.tag=v1.0.1 -n todo-chatbot-dev`
5. Verify: `kubectl rollout status deployment/todo-chatbot-frontend -n todo-chatbot-dev`

---

## 🤝 Contributing

This project follows spec-driven development principles. All infrastructure is defined in specifications and generated through automation.

**Governance**: See [`.specify/memory/constitution.md`](../.specify/memory/constitution.md)

---

## 📄 License

This project is part of the Hackathone2 repository.

---

**Status**: ✅ **MVP READY** - Deploy locally today! 🚀
