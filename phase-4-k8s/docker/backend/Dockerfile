# =============================================================================
# Multi-Stage Dockerfile for FastAPI Backend
# Target: < 200MB compressed image size
# Base: python:3.12-slim
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements file from backend directory
COPY phase-3-chatbot/backend/requirements.txt .

# Install Python dependencies to temporary location
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Runtime
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install runtime dependencies (only postgresql-client for health checks)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1000 appuser

# Copy Python dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code from phase-3-chatbot/backend
COPY phase-3-chatbot/backend/requirements.txt .
COPY phase-3-chatbot/backend/main.py .
COPY phase-3-chatbot/backend/db.py .
COPY phase-3-chatbot/backend/models ./models
COPY phase-3-chatbot/backend/routes ./routes
COPY phase-3-chatbot/backend/services ./services
COPY phase-3-chatbot/backend/agents ./agents
COPY phase-3-chatbot/backend/auth ./auth
COPY phase-3-chatbot/backend/schemas ./schemas
COPY phase-3-chatbot/backend/mcp_tools ./mcp_tools

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/tmp && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start FastAPI application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
