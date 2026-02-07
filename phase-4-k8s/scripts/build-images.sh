#!/bin/bash
# =============================================================================
# Docker Image Build Script for Todo AI Chatbot
# Purpose: Build and load frontend/backend images into Minikube
# =============================================================================

set -e  # Exit on error

echo "🐳 Building Docker images for Todo AI Chatbot..."
echo ""

# Get project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# =============================================================================
# Build Frontend Image
# =============================================================================
echo "📦 Building frontend image (todo-chatbot-frontend:v1.0.0)..."
docker build \
    -t todo-chatbot-frontend:v1.0.0 \
    -f phase-4-k8s/docker/frontend/Dockerfile \
    .

echo "✅ Frontend image built successfully"

# Show frontend image size
FRONTEND_SIZE=$(docker images todo-chatbot-frontend:v1.0.0 --format "{{.Size}}")
echo "   Size: $FRONTEND_SIZE"
echo ""

# =============================================================================
# Build Backend Image
# =============================================================================
echo "📦 Building backend image (todo-chatbot-backend:v1.0.0)..."
docker build \
    -t todo-chatbot-backend:v1.0.0 \
    -f phase-4-k8s/docker/backend/Dockerfile \
    .

echo "✅ Backend image built successfully"

# Show backend image size
BACKEND_SIZE=$(docker images todo-chatbot-backend:v1.0.0 --format "{{.Size}}")
echo "   Size: $BACKEND_SIZE"
echo ""

# =============================================================================
# Load Images into Minikube
# =============================================================================
echo "📥 Loading images into Minikube..."
minikube image load todo-chatbot-frontend:v1.0.0
echo "✅ Frontend image loaded into Minikube"
minikube image load todo-chatbot-backend:v1.0.0
echo "✅ Backend image loaded into Minikube"
echo ""

# =============================================================================
# Verify Images
# =============================================================================
echo "🔍 Verifying images..."
docker images | grep "todo-chatbot"

echo ""
echo "✅ Image build complete!"
echo ""
echo "Next steps:"
echo "  1. Deploy: ./scripts/deploy.sh"
echo "  2. Test: ./scripts/test-deployment.sh"
echo ""
