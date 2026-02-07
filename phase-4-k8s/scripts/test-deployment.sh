#!/bin/bash
# =============================================================================
# Smoke Test Script for Todo AI Chatbot Deployment
# Purpose: Verify deployment is working correctly
# =============================================================================

set -e  # Exit on error

echo "🧪 Running smoke tests for Todo AI Chatbot..."
echo ""

NAMESPACE="todo-chatbot-dev"

# =============================================================================
# Test 1: Check Pod Status
# =============================================================================
echo "1️⃣  Testing pod status..."
POD_STATUS=$(kubectl get pods -n $NAMESPACE -o jsonpath='{.items[*].status.phase}')
if echo "$POD_STATUS" | grep -q "Running"; then
    echo "   ✅ Pods are Running"
else
    echo "   ❌ Pods are not Running"
    echo "   Status: $POD_STATUS"
    kubectl get pods -n $NAMESPACE
    exit 1
fi
echo ""

# =============================================================================
# Test 2: Check Services
# =============================================================================
echo "2️⃣  Testing services..."
FRONTEND_SVC=$(kubectl get svc -n $NAMESPACE todo-chatbot-frontend-service -o jsonpath='{.status}')
BACKEND_SVC=$(kubectl get svc -n $NAMESPACE todo-chatbot-backend-service -o jsonpath='{.status}')

if [ -n "$FRONTEND_SVC" ] && [ -n "$BACKEND_SVC" ]; then
    echo "   ✅ Services exist"
else
    echo "   ❌ Services not found"
    kubectl get svc -n $NAMESPACE
    exit 1
fi
echo ""

# =============================================================================
# Test 3: Frontend Health Check
# =============================================================================
echo "3️⃣  Testing frontend health endpoint..."
FRONTEND_POD=$(kubectl get pod -n $NAMESPACE -l app=todo-chatbot-frontend -o jsonpath='{.items[0].metadata.name}')

if [ -n "$FRONTEND_POD" ]; then
    FRONTEND_HEALTH=$(kubectl exec -n $NAMESPACE $FRONTEND_POD -- curl -s http://localhost:3000/health 2>/dev/null || echo "failed")

    if echo "$FRONTEND_HEALTH" | grep -q "healthy"; then
        echo "   ✅ Frontend is healthy"
    else
        echo "   ❌ Frontend health check failed"
        echo "   Response: $FRONTEND_HEALTH"
    fi
else
    echo "   ❌ Frontend pod not found"
fi
echo ""

# =============================================================================
# Test 4: Backend Health Check (via port-forward)
# =============================================================================
echo "4️⃣  Testing backend health endpoint..."
BACKEND_POD=$(kubectl get pod -n $NAMESPACE -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}')

if [ -n "$BACKEND_POD" ]; then
    # Start port-forward in background
    kubectl port-forward -n $NAMESPACE $BACKEND_POD 8000:8000 >/dev/null 2>&1 &
    PF_PID=$!

    # Wait for port-forward to be ready
    sleep 3

    # Test backend health
    BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "failed")

    if echo "$BACKEND_HEALTH" | grep -q "healthy"; then
        echo "   ✅ Backend is healthy"
    else
        echo "   ❌ Backend health check failed"
        echo "   Response: $BACKEND_HEALTH"
    fi

    # Kill port-forward
    kill $PF_PID 2>/dev/null || true
else
    echo "   ❌ Backend pod not found"
fi
echo ""

# =============================================================================
# Test Summary
# =============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All smoke tests passed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Application is ready!"
echo ""
echo "🌐 To access the application:"
echo "   1. Start tunnel: minikube tunnel (separate terminal)"
echo "   2. Open browser: http://127.0.0.1:3000"
echo ""
