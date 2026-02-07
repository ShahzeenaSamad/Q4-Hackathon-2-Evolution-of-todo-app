#!/bin/bash
# =============================================================================
# Teardown Script for Todo AI Chatbot
# Purpose: Remove all Kubernetes resources cleanly
# =============================================================================

set -e  # Exit on error

echo "🗑️  Tearing down Todo AI Chatbot deployment..."
echo ""

NAMESPACE="todo-chatbot-dev"

# =============================================================================
# Option to completely delete Minikube cluster
# =============================================================================
if [ "$1" == "--delete-cluster" ]; then
    echo "⚠️  Deleting entire Minikube cluster..."
    minikube delete
    echo "✅ Minikube cluster deleted"
    echo ""
    echo "To recreate, run: ./scripts/setup-minikube.sh"
    exit 0
fi

# =============================================================================
# Uninstall Helm Release
# =============================================================================
echo "📦 Uninstalling Helm chart..."
if helm list -n $NAMESPACE | grep -q "todo-chatbot"; then
    helm uninstall todo-chatbot -n $NAMESPACE
    echo "✅ Helm chart uninstalled"
else
    echo "⚠️  Helm release not found (already uninstalled?)"
fi
echo ""

# =============================================================================
# Delete Namespace
# =============================================================================
echo "🗑️  Deleting namespace: $NAMESPACE"
if kubectl get namespace $NAMESPACE &>/dev/null; then
    kubectl delete namespace $NAMESPACE
    echo "✅ Namespace deleted"
else
    echo "⚠️  Namespace not found (already deleted?)"
fi
echo ""

# =============================================================================
# Verify Cleanup
# =============================================================================
echo "🔍 Verifying cleanup..."
REMAINING_PODS=$(kubectl get pods -n $NAMESPACE 2>/dev/null | grep -v "No resources found" | wc -l)

if [ "$REMAINING_PODS" -eq 0 ]; then
    echo "✅ All resources cleaned up successfully"
else
    echo "⚠️  Some resources still exist:"
    kubectl get all -n $NAMESPACE
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Teardown complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔄 To redeploy:"
echo "   1. ./scripts/setup-minikube.sh (if needed)"
echo "   2. ./scripts/build-images.sh"
echo "   3. ./scripts/deploy.sh"
echo ""
echo "💡 To delete entire Minikube cluster:"
echo "   ./scripts/teardown.sh --delete-cluster"
echo ""
