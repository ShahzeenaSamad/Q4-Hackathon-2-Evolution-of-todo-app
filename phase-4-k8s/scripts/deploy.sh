#!/bin/bash
# =============================================================================
# Deployment Script for Todo AI Chatbot
# Purpose: Deploy chatbot to Minikube using Helm
# =============================================================================

set -e  # Exit on error

echo "🚀 Deploying Todo AI Chatbot to Minikube..."
echo ""

# Get project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ ERROR: OPENAI_API_KEY environment variable not set"
    echo ""
    echo "Please set your OpenAI API key:"
    echo "  export OPENAI_API_KEY='sk-your-actual-key-here'"
    echo ""
    exit 1
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  WARNING: DATABASE_URL not set, using default"
    DATABASE_URL="postgresql://todo_user:password@ep-cool-neon.aws.neon.tech/todo_db"
fi

# =============================================================================
# Create Secrets
# =============================================================================
echo "🔐 Creating Kubernetes secrets..."
kubectl create secret generic backend-secrets \
    --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
    -n todo-chatbot-dev \
    --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Secrets created"
echo ""

# =============================================================================
# Install/Upgrade Helm Chart
# =============================================================================
echo "📦 Installing Helm chart..."
helm upgrade --install todo-chatbot ./phase-4-k8s/helm \
    --namespace todo-chatbot-dev \
    --values phase-4-k8s/helm/values-dev.yaml \
    --set backend.secrets.OPENAI_API_KEY="$OPENAI_API_KEY" \
    --wait \
    --timeout 5m

echo ""
echo "✅ Helm chart installed successfully"
echo ""

# =============================================================================
# Wait for Rollouts
# =============================================================================
echo "⏳ Waiting for deployments to be ready..."
kubectl rollout status deployment/todo-chatbot-frontend -n todo-chatbot-dev
kubectl rollout status deployment/todo-chatbot-backend -n todo-chatbot-dev

echo ""
echo "✅ All deployments are ready!"
echo ""

# =============================================================================
# Display Pod Status
# =============================================================================
echo "📊 Current pod status:"
kubectl get pods -n todo-chatbot-dev

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Next steps:"
echo "  1. Start Minikube tunnel (in separate terminal):"
echo "     minikube tunnel"
echo ""
echo "  2. Access the application at:"
echo "     http://127.0.0.1:3000"
echo ""
echo "  3. Run tests:"
echo "     ./scripts/test-deployment.sh"
echo ""
