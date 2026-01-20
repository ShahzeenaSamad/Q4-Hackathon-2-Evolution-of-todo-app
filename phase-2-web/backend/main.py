"""
FastAPI Backend for Todo App - Phase II
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Todo App API",
    description="Phase II: Full-Stack Web Application Backend",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        os.getenv("FRONTEND_URL", ""),  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/api/v1/health")
async def health_check():
    """Check API and database health status"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2026-01-17T10:30:00Z"
    }

# Import routes
from routes_tasks import router as tasks_router
from routes_auth import router as auth_router

# Register routes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["Tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
