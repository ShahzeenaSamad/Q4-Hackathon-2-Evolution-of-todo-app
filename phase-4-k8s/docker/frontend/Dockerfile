# =============================================================================
# Multi-Stage Dockerfile for Next.js Frontend
# Target: < 100MB compressed image size
# Base: node:20-alpine
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Dependencies
# -----------------------------------------------------------------------------
FROM node:20-alpine AS dependencies

# Set working directory
WORKDIR /app

# Copy package files from frontend
COPY frontend/package*.json ./

# Install ALL dependencies (including dev dependencies for build)
RUN npm install && \
    npm cache clean --force

# -----------------------------------------------------------------------------
# Stage 2: Builder
# -----------------------------------------------------------------------------
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy dependencies from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy frontend source code from root directory
COPY frontend/package*.json ./
COPY frontend/tsconfig.json ./
COPY frontend/next.config.js ./
COPY frontend/tailwind.config.ts ./
COPY frontend/postcss.config.js ./
COPY frontend/app ./app
COPY frontend/components ./components
COPY frontend/lib ./lib

# Build arguments
ARG NEXT_PUBLIC_API_URL=http://backend-service:8000
ARG NEXT_PUBLIC_APP_NAME=Todo AI Chatbot
ARG NEXT_PUBLIC_ENVIRONMENT=production

# Set environment variables during build
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_PUBLIC_APP_NAME=${NEXT_PUBLIC_APP_NAME}
ENV NEXT_PUBLIC_ENVIRONMENT=${NEXT_PUBLIC_ENVIRONMENT}

# Build Next.js application
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 3: Runner (Production Runtime)
# -----------------------------------------------------------------------------
FROM node:20-alpine AS runner

# Set working directory
WORKDIR /app

# Install dependencies
RUN npm install next@latest

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy application from builder
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/app ./app
COPY --from=builder /app/components ./components
COPY --from=builder /app/lib ./lib
COPY --from=builder /app/tsconfig.json ./
COPY --from=builder /app/next.config.js ./

# Set ownership to non-root user
RUN chown -R nextjs:nodejs /app

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start Next.js application
CMD ["npm", "start"]
