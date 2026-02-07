#!/bin/bash
# =============================================================================
# Minikube Setup Script for Todo AI Chatbot (8GB RAM Optimized)
# Purpose: Start Minikube cluster with conservative resource allocation
# =============================================================================

set -e  # Exit on error

echo "🚀 Setting up Minikube for Todo AI Chatbot (8GB RAM Optimized)..."
echo ""

# Check if Minikube is running
if minikube status &>/dev/null; then
    echo "✅ Minikube is already running"
    echo ""
    echo "Current resource allocation:"
    minikube config view | grep -E "(memory|cpus)" || echo "  Using defaults"
    echo ""
    minikube status
else
    echo "📍 Starting Minikube with Docker driver (8GB optimized)..."
    echo ""
    echo "Resource Allocation:"
    echo "  - CPUs: 2 cores (conservative for 8GB system)"
    echo "  - Memory: 3584MB (~3.5GB, safe for 8GB system)"
    echo "  - Disk: 20GB"
    echo ""

    minikube start \
        --driver=docker \
        --cpus=2 \
        --memory=3584 \
        --disk-size=20000mb \
        --extra-config=kubelet.resolv-conf=/run/systemd/resolve/resolv.conf

    echo ""
    echo "✅ Minikube started successfully"
fi

# Enable required add-ons
echo ""
echo "🔧 Enabling Minikube add-ons..."
minikube addons enable dashboard &>/dev/null || echo "  ⚠️  Dashboard already enabled"
minikube addons enable metrics-server &>/dev/null || echo "  ⚠️  Metrics-server already enabled"
echo "✅ Add-ons enabled (dashboard, metrics-server)"

# Create namespace
echo ""
echo "📦 Creating namespace: todo-chatbot-dev"
if kubectl get namespace todo-chatbot-dev &>/dev/null; then
    echo "⚠️  Namespace already exists"
else
    kubectl create namespace todo-chatbot-dev
    echo "✅ Namespace created"
fi

# Verify cluster status
echo ""
echo "🔍 Verifying cluster status..."
kubectl get nodes
echo ""
kubectl get namespace todo-chatbot-dev

# Check node resources
echo ""
echo "💾 Node resource capacity:"
kubectl describe node | grep -A 3 "Allocated resources"

echo ""
echo "✅ Minikube setup complete!"
echo ""
echo "📊 Resource Summary:"
echo "  - Cluster: Minikube (Docker driver)"
echo "  - Namespace: todo-chatbot-dev"
echo "  - Safe for development on 8GB systems"
echo ""
echo "Next steps:"
echo "  1. Build images:   ./scripts/build-images.sh"
echo "  2. Set API key:    export OPENAI_API_KEY='sk-...'"
echo "  3. Deploy:         ./scripts/deploy.sh"
echo "  4. Start tunnel:   minikube tunnel (separate terminal)"
echo ""
