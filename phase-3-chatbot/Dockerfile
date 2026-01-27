# Phase 3 AI Chatbot Backend - Dockerfile for Hugging Face Spaces
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (FastAPI runs on 8000 by default, but we'll use 7860 for HF Spaces)
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=7860

# Health check
HEALTHCHECK CMD curl -f http://localhost:7860/ || exit 1

# Run the application (using uvicorn for production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
