#!/bin/bash
# =============================================================================
# Minikube Setup Script for Todo AI Chatbot
# Purpose: Start Minikube cluster and configure namespace
# =============================================================================

set -e  # Exit on error

echo "🚀 Setting up Minikube for Todo AI Chatbot..."

# Check if Minikube is running
if minikube status &>/dev/null; then
    echo "✅ Minikube is already running"
    minikube status
else
    echo "📍 Starting Minikube with Docker driver..."
    minikube start \
        --driver=docker \
        --cpus=4 \
        --memory=8192 \
        --disk-size=20000mb

    echo "✅ Minikube started successfully"
fi

# Enable required add-ons
echo ""
echo "🔧 Enabling Minikube add-ons..."
minikube addons enable dashboard &>/dev/null || true
minikube addons enable metrics-server &>/dev/null || true
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

echo ""
echo "✅ Minikube setup complete!"
echo ""
echo "Next steps:"
echo "  1. Build images: ./scripts/build-images.sh"
echo "  2. Deploy: ./scripts/deploy.sh"
echo "  3. Start tunnel (in separate terminal): minikube tunnel"
echo ""
