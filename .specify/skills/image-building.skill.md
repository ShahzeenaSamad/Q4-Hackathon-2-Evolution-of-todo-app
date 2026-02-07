# Docker Image Building Skill

## Description
Reusable skill for building, managing, and optimizing Docker images for Kubernetes deployment. Includes building strategies, tagging, registry management, and CI/CD integration.

## When to Use
- Building Docker images for frontend and backend services
- Managing image versions and tags
- Pushing images to container registries
- Implementing build optimization strategies
- Setting up automated image builds (CI/CD)

## Capabilities

### 1. Build Docker Images
```bash
# Basic build
docker build -t todo-app:latest .

# Build with context and Dockerfile
docker build -f Dockerfile.frontend -t todo-frontend:v1.0.0 ./frontend

# Build with build arguments
docker build \
  --build-arg NODE_ENV=production \
  --build-arg NEXT_PUBLIC_API_URL=https://api.example.com \
  -t todo-frontend:prod \
  ./frontend

# Build with BuildKit (recommended)
DOCKER_BUILDKIT=1 docker build -t todo-app:latest .

# Build for specific platform
docker buildx build --platform linux/amd64 -t todo-app:latest .
```

### 2. Image Tagging Strategies
```bash
# Semantic versioning
docker build -t todo-frontend:1.0.0 .
docker build -t todo-frontend:1.0 .
docker build -t todo-frontend:1 .
docker build -t todo-frontend:latest .

# Git commit based
docker build -t todo-frontend:$(git rev-parse --short HEAD) .
docker build -t todo-frontend:branch-$(git rev-parse --abbrev-ref HEAD) .

# Date-based
docker build -t todo-frontend:$(date +%Y%m%d) .

# Environment-based
docker build -t todo-frontend:dev .
docker build -t todo-frontend:staging .
docker build -t todo-frontend:production .
```

### 3. Multi-Architecture Builds
```bash
# Enable buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t todo-app:latest \
  --push \
  .

# Build and load for local testing
docker buildx build \
  --platform linux/amd64 \
  -t todo-app:latest \
  --load \
  .
```

### 4. Push to Container Registries

#### Docker Hub
```bash
# Login
docker login

# Tag and push
docker tag todo-frontend:latest username/todo-frontend:latest
docker tag todo-frontend:latest username/todo-frontend:v1.0.0
docker push username/todo-frontend:latest
docker push username/todo-frontend:v1.0.0
```

#### GitHub Container Registry (GHCR)
```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag and push
docker tag todo-frontend:latest ghcr.io/username/todo-frontend:latest
docker tag todo-frontend:latest ghcr.io/username/todo-frontend:v1.0.0
docker push ghcr.io/username/todo-frontend:latest
docker push ghcr.io/username/todo-frontend:v1.0.0
```

#### Azure Container Registry (ACR)
```bash
# Login
az acr login --name myregistry

# Tag and push
docker tag todo-frontend:latest myregistry.azurecr.io/todo-frontend:latest
docker push myregistry.azurecr.io/todo-frontend:latest
```

### 5. Build Automation with Docker Compose
```yaml
# docker-compose.build.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
      cache_from:
        - todo-frontend:latest
      target: runner
    image: todo-frontend:${TAG:-latest}

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      cache_from:
        - todo-backend:latest
    image: todo-backend:${TAG:-latest}
```

**Usage:**
```bash
# Build all services
docker-compose -f docker-compose.build.yml build

# Build with custom tag
TAG=v1.0.0 docker-compose -f docker-compose.build.yml build

# Build specific service
docker-compose -f docker-compose.build.yml build frontend
```

## Optimization Strategies

### 1. Layer Caching
```dockerfile
# Good: Layers cached independently
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./  # Cache this layer
RUN npm install                          # Cache this layer
COPY . .                                # Only rebuild when code changes

# Bad: No caching optimization
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install  # Runs every time any file changes
```

### 2. Multi-Stage Build Optimization
```dockerfile
# Builder stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runner stage - minimal final image
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### 3. BuildKit Features
```bash
# Enable BuildKit features
DOCKER_BUILDKIT=1 docker build .

# Use cache mounts
docker build \
  --mount type=cache,target=/root/.npm \
  -t todo-app:latest .

# Use secret mounts
docker build \
  --secret id=npm_token,env=NPM_TOKEN \
  -t todo-app:latest .
```

### 4. Image Size Reduction
```bash
# Scan image for vulnerabilities
docker scan todo-app:latest

# Analyze image layers
docker history todo-app:latest

# View image details
docker inspect todo-app:latest

# Find large files in image
docker run --rm -it todo-app:latest sh -c "du -sh /* | sort -hr"
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Images

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/username/todo-app
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitLab CI
```yaml
# .gitlab-ci.yml
build-image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
```

## Testing Images

### Local Testing
```bash
# Build image
docker build -t test-app:latest .

# Run container
docker run -d -p 3000:3000 --name test-container test-app:latest

# Wait for startup
sleep 5

# Test health endpoint
curl http://localhost:3000/health

# View logs
docker logs test-container

# Clean up
docker stop test-container
docker rm test-container
```

### Integration Testing
```bash
# Build and run with docker-compose
docker-compose -f docker-compose.test.yml up -d

# Run tests
docker-compose exec backend pytest

# Check coverage
docker-compose exec backend pytest --cov=.

# Clean up
docker-compose -f docker-compose.test.yml down
```

## Image Management

### List and Inspect Images
```bash
# List all images
docker images

# List dangling images
docker images -f dangling=true

# Inspect image
docker inspect todo-app:latest

# View image history
docker history todo-app:latest --human

# Show image disk usage
docker system df -v
```

### Clean Up Images
```bash
# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Remove specific image
docker rmi todo-app:latest

# Force remove
docker rmi -f todo-app:latest

# Remove all images
docker rmi $(docker images -q)
```

### Tag Management
```bash
# Retag image
docker tag todo-app:latest todo-app:v1.0.0

# Push all tags
docker push --all-tags username/todo-app

# Remove remote tag (use API)
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  https://ghcr.io/v2/username/todo-app/manifests/latest
```

## Best Practices

### 1. Use Specific Versions
```bash
# Good: Use specific versions
FROM node:20.11.0-alpine

# Bad: Use latest
FROM node:latest
```

### 2. Minimize Layers
```dockerfile
# Good: Combine RUN commands
RUN apt-get update && \
    apt-get install -y gcc postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Bad: Multiple RUN commands
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y postgresql-client
```

### 3. Leverage Build Cache
```bash
# Build with cache
docker build -t app:latest .

# Use cache from previous build
docker build \
  --cache-from app:latest \
  -t app:new .
```

### 4. Security Scanning
```bash
# Scan for vulnerabilities
docker scan todo-app:latest

# Scan with Trivy
trivy image todo-app:latest

# Fix vulnerabilities
docker pull todo-app:latest
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image todo-app:latest
```

## Error Handling

### Build Failures
```bash
# Debug build failures
docker build --progress=plain -t app:latest .

# Build without cache
docker build --no-cache -t app:latest .

# Check Dockerfile syntax
docker build --check -f Dockerfile .

# Inspect build cache
docker builder prune
```

### Push Failures
```bash
# Check login status
docker login

# Retry push
docker push todo-app:latest

# Use retry logic
for i in {1..3}; do docker push todo-app:latest && break || sleep 5; done
```

## Performance Metrics

### Build Time Optimization
```bash
# Measure build time
time docker build -t app:latest .

# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t app:latest .

# Parallel builds
docker build -t frontend:latest ./frontend & \
docker build -t backend:latest ./backend & \
wait
```

### Image Size Metrics
```bash
# Compare image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Find largest images
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}" | \
  sort -k2 -h | tail -5
```

## Dependencies
- Docker 20.10+ or Docker Desktop 4.53+
- docker buildx (for multi-platform builds)
- Container registry access (Docker Hub, GHCR, ACR, etc.)
- CI/CD platform (optional, for automation)

## Integration with Kubernetes
- Images are ready for Kubernetes deployment
- Multi-platform builds support different cluster architectures
- Health checks integrate with Kubernetes probes
- Small image sizes enable faster deployments
- Version tagging enables rolling updates
