# Dockerfile Generation Skill

## Description
Reusable skill for generating optimized Dockerfiles for Next.js frontend and FastAPI backend applications. Supports multi-stage builds, caching, and production-ready configurations.

## When to Use
- Containerizing Next.js frontend applications
- Containerizing FastAPI backend services
- Preparing applications for Kubernetes deployment
- Creating production-ready container images
- Implementing Docker best practices (multi-stage builds, layer caching)

## Capabilities

### 1. Generate Next.js Frontend Dockerfile
```dockerfile
# Dockerfile.frontend
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.js collects completely anonymous telemetry data
ENV NEXT_TELEMETRY_DISABLED=1

# Build the application
RUN \
  if [ -f yarn.lock ]; then yarn run build; \
  elif [ -f package-lock.json ]; then npm run build; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

**Usage:**
```bash
# Build the image
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Run the container
docker run -p 3000:3000 todo-frontend:latest
```

### 2. Generate FastAPI Backend Dockerfile
```dockerfile
# Dockerfile.backend
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Usage:**
```bash
# Build the image
docker build -f Dockerfile.backend -t todo-backend:latest .

# Run with environment variables
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e OPENAI_API_KEY=sk-... \
  todo-backend:latest
```

### 3. Generate Multi-Service Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    networks:
      - todo-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
    depends_on:
      - db
    networks:
      - todo-network
    volumes:
      - backend-data:/app/data

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=todo
      - POSTGRES_PASSWORD=todo
      - POSTGRES_DB=todo
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - todo-network

networks:
  todo-network:
    driver: bridge

volumes:
  db-data:
  backend-data:
```

**Usage:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Configuration Examples

### Next.js Configuration (next.config.js)
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // Required for Docker deployment
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
}

module.exports = nextConfig
```

### .dockerignore for Frontend
```
node_modules
.next
.git
.gitignore
README.md
Dockerfile
.dockerignore
npm-debug.log
yarn-error.log
.vercel
.env*.local
```

### .dockerignore for Backend
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.so
.git
.gitignore
README.md
Dockerfile
.dockerignore
.pytest_cache
.coverage
dist
build
*.egg-info
```

## Best Practices

### 1. Multi-Stage Builds
- Separate build and runtime dependencies
- Minimize final image size
- Only include production artifacts in final image

### 2. Layer Caching
- Copy dependency files first (package.json, requirements.txt)
- Install dependencies before copying source code
- Order Dockerfile instructions from least to most frequently changing

### 3. Security
- Use non-root users
- Run as read-only where possible
- Scan images for vulnerabilities
- Use specific version tags (not `latest`)

### 4. Environment Variables
- Never hardcode secrets in Dockerfile
- Use ENV for configuration
- Pass sensitive data at runtime

### 5. Health Checks
- Define HEALTHCHECK for all services
- Check application readiness, not just process status
- Set appropriate intervals and timeouts

## Common Dockerfile Patterns

### Development Dockerfile (with hot reload)
```dockerfile
# Dockerfile.dev
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
```

### Production Dockerfile (optimized)
```dockerfile
# Use the multi-stage build examples above
# They include:
# - Separate builder and runner stages
# - Minimal final image size
# - Security best practices
# - Health checks
```

## Error Handling

### Build Failures
```bash
# Build with no cache to troubleshoot
docker build --no-cache -t myapp:latest .

# Build with verbose output
docker build --progress=plain -t myapp:latest .

# Check layer contents
docker history myapp:latest
```

### Runtime Issues
```bash
# View container logs
docker logs <container_id>

# Execute into container
docker exec -it <container_id> /bin/sh

# Check container health
docker inspect <container_id> --format='{{.State.Health.Status}}'
```

## Testing Dockerfiles

### Local Testing
```bash
# Build image
docker build -t test-app:latest .

# Run container
docker run -p 3000:3000 test-app:latest

# Test health endpoint
curl http://localhost:3000/health

# Clean up
docker stop $(docker ps -q) && docker system prune -f
```

### Integration Testing
```bash
# Test with docker-compose
docker-compose up -d
docker-compose ps
docker-compose logs frontend
docker-compose exec backend python -m pytest
docker-compose down
```

## Optimization Tips

1. **Use .dockerignore**: Exclude unnecessary files from build context
2. **Leverage BuildKit**: `DOCKER_BUILDKIT=1 docker build .`
3. **Parallel builds**: Build multiple images simultaneously
4. **Base image selection**: Use `alpine` variants for smaller images
5. **Dependency caching**: Cache dependencies separately from source code

## Dependencies
- Docker 20.10+ or Docker Desktop 4.53+
- Next.js 16+ for frontend Dockerfiles
- Python 3.13+ for backend Dockerfiles
- docker-compose (optional, for local development)

## Integration with Kubernetes
These Dockerfiles are designed to work seamlessly with Kubernetes deployments:
- Images can be pushed to container registries (Docker Hub, GHCR)
- Multi-stage builds produce minimal images for faster deployments
- Health checks integrate with Kubernetes probes
- Non-root users comply with Pod Security Policies
